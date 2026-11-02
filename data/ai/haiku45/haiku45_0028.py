import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Initialize the game board with empty spaces."""
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """Print the game board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLUMNS + "+")


def get_valid_input(board, current_player_checker):
    """Get and validate user input for column selection."""
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid column letter
        if user_input < 'A' or user_input >= chr(65 + COLUMNS):
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLUMNS)}.")
            continue
        
        col = ord(user_input) - 65
        
        # Check if column is full
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1


def check_horizontal_win(board, checker):
    """Check if there is a horizontal win for the given checker."""
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker):
    """Check if there is a vertical win for the given checker."""
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker):
    """Check if there is a diagonal win (both directions) for the given checker."""
    # Check diagonal going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """Check if the given checker has won the game."""
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def get_player_checkers():
    """Get the checkers for the current game based on number of players."""
    return PLAYER_CHECKERS[:NUM_PLAYERS]


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Get player checkers
    player_checkers = get_player_checkers()
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = player_checkers[current_player_index]
        
        # Get valid column input from player
        col = get_valid_input(board, current_checker)
        
        # Place checker on board
        place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Main function to start the game."""
    play_game()


if __name__ == "__main__":
    main()
