import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
WIN_LENGTH = 4
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and initialize the game board with empty spaces."""
    board = []
    for row in range(BOARD_ROWS):
        new_row = []
        for col in range(BOARD_COLS):
            new_row.append(" ")
        board.append(new_row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(BOARD_COLS):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with rows
    for row in range(BOARD_ROWS):
        # Print top border
        print("+---" * BOARD_COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(BOARD_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * BOARD_COLS + "+")

def get_valid_column():
    """Get a valid column input from the user."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board
        if col_index < 0 or col_index >= BOARD_COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + BOARD_COLS - 1)}.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column and return True if successful."""
    # Find the lowest empty row in the column
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("That column is full. Please choose another column.")
    return False

def check_horizontal_win(board, checker):
    """Check if there is a horizontal win for the checker."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - WIN_LENGTH + 1):
            # Check if all 4 consecutive cells have the checker
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_vertical_win(board, checker):
    """Check if there is a vertical win for the checker."""
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - WIN_LENGTH + 1):
            # Check if all 4 consecutive cells have the checker
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal_win(board, checker):
    """Check if there is a diagonal win for the checker."""
    # Check diagonals going down-right
    for row in range(BOARD_ROWS - WIN_LENGTH + 1):
        for col in range(BOARD_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(BOARD_ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, checker):
    """Check if the specified checker has won."""
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))

def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get player checkers
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Choose random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid column from player
        print(f"Player {current_checker}, please enter a column: ", end="")
        col = get_valid_column()
        
        # Try to place checker, keep asking until valid placement
        while not place_checker(board, col, current_checker):
            print(f"Player {current_checker}, please enter a column: ", end="")
            col = get_valid_column()
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print(f"Player {players[current_player_index]}, please enter a column: ", end="")

def main():
    """Start the game."""
    play_game()

if __name__ == "__main__":
    main()
