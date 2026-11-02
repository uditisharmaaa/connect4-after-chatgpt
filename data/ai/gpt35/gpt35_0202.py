import os
import random

# Constants for board dimensions and players
ROWS = 6          # Number of rows
COLS = 7          # Number of columns (max 26)
NUM_PLAYERS = 2   # Number of players (2 to 5)
WIN_LENGTH = 4    # Number of checkers in a row to win

# List of player checkers in order
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Use only the number of players specified
PLAYERS = PLAYER_CHECKERS[:NUM_PLAYERS]

def clear_screen():
    """Clear the game screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board():
    """Create initially empty board filled with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect 4 board with column labels and separators."""
    # Print column headers (A, B, C, ...)
    headers = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS))
    print(headers)
    # Print rows with separators
    for r in range(ROWS):
        print('+' + '---+' * COLS)
        row_str = '|'
        for c in range(COLS):
            row_str += f' {board[r][c]} |'
        print(row_str)
    print('+' + '---+' * COLS)

def is_valid_column(col_char):
    """Check if column character is valid (A to A+COLS-1)."""
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    return 0 <= col < COLS

def get_column_index(col_char):
    """Convert column character (A-G) to index (0-6)."""
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in the lowest empty row in the given column.
    Return True if placed successfully, False if column is full.
    """
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the given player has 4 in a row anywhere on the board."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True
    # Check diagonal (down-right)
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Check diagonal (up-right)
    for r in range(WIN_LENGTH - 1, ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    # If any space in top row is empty, board is not full
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_player_input(current_player):
    """
    Prompt the player to enter a valid column letter.
    Validate input and repeat until valid.
    """
    while True:
        col_char = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not is_valid_column(col_char):
            # Invalid character or out of range
            continue
        col = get_column_index(col_char)
        return col_char, col

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()

    # Randomly select first player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        current_checker = PLAYERS[current_player_idx]

        col_char, col = get_player_input(current_checker)

        # Try to place checker
        placed = place_checker(board, col, current_checker)
        if not placed:
            # Column full -> player loses turn
            # Just switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_winner(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
