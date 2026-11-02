import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, rows, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * cols + "+")


def is_valid_input(column_letter, cols):
    """Validate the column input from the player."""
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isalpha():
        return False
    
    column_index = ord(column_letter.upper()) - ord('A')
    
    if column_index < 0 or column_index >= cols:
        return False
    
    return True


def get_column_index(column_letter):
    """Convert column letter to column index."""
    return ord(column_letter.upper()) - ord('A')


def is_column_full(board, col_index, rows):
    """Check if a column is completely full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker, rows, cols):
    """Place a checker in the specified column. Returns True if successful."""
    if is_column_full(board, col_index, rows):
        return False
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_winner(board, rows, cols, checker):
    """Check if the specified checker has won."""
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board, rows, cols):
    """Check if the board is completely full (draw condition)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def get_player_move(player_checker, cols):
    """Get valid input from the player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if not is_valid_input(user_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(user_input)
        return col_index


def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLS)
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board, ROWS, COLS)
    
    while True:
        current_checker = checkers[current_player_index]
        
        # Get valid move from current player
        col_index = get_player_move(current_checker, COLS)
        
        # Try to place the checker
        if not place_checker(board, col_index, current_checker, ROWS, COLS):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board, ROWS, COLS)
        
        # Check for win
        if check_winner(board, ROWS, COLS, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
