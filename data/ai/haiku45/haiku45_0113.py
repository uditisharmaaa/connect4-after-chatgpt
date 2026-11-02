import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def is_valid_input(col_letter):
    """Check if the input is a valid column letter."""
    if len(col_letter) != 1:
        return False
    
    if not col_letter.isupper():
        return False
    
    col_index = ord(col_letter) - ord('A')
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    return True


def get_player_input(player_checker):
    """Get valid column input from the player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column letter (A-" + chr(ord('A') + COLS - 1) + ").")
            continue
        
        col_index = ord(user_input) - ord('A')
        return col_index


def is_column_full(board, col_index):
    """Check if a column is completely full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """Place a checker in the specified column and return True if successful."""
    if is_column_full(board, col_index):
        print("This column is full. Please choose another column.")
        return False
    
    # Find the lowest empty row in this column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """Check if there is a horizontal win for the given checker."""
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker):
    """Check if there is a vertical win for the given checker."""
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker):
    """Check if there is a diagonal win for the given checker."""
    # Check diagonals going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    if check_horizontal_win(board, checker):
        return True
    if check_vertical_win(board, checker):
        return True
    if check_diagonal_win(board, checker):
        return True
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Choose a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    # Main game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        
        # Get valid column input from player
        col_index = get_player_input(current_checker)
        
        # Try to place the checker
        if not place_checker(board, col_index, current_checker):
            # If placement failed (column full), ask again without changing turn
            continue
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            return
        
        # Check if board is full (draw)
        if is_board_full(board):
            print("It's a draw!")
            return
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
