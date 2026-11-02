import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns supported by labels A-Z
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization ---
def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear')  # Clear screen for Linux/Unix
    
    # Print column labels (A, B, C...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    
    # Print board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_content = []
        for c in range(len(board[0])):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")
    print("+---" * len(board[0]) + "+")

# --- Game Logic ---
def get_column_input(current_player_checker, num_cols):
    """Prompts the current player for a column input and validates it."""
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= chr(ord('A') + num_cols - 1):
                raise ValueError
            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError:
            print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}.")

def place_checker(board, col_index, checker):
    """Places the checker in the lowest available space in the given column.
    Returns True if successful, False if the column is full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """Checks if the given checker has 4 in a row horizontally, vertically, or diagonally."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full, indicating a draw."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Function ---
def play_connect_4():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        current_player_checker = players[current_player_index]
        print_board(board)
        
        col_index = get_column_input(current_player_checker, NUM_COLS)

        if place_checker(board, col_index, current_player_checker):
            # Check for win
            if check_win(board, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                break
            
            # Check for draw
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn if column is full, they are prompted again in the loop

if __name__ == "__main__":
    play_connect_4()
