import os
import random
import string
import sys

# ----- Configuration constants -----
ROWS = 6                 # number of rows (height)
COLS = 7                 # number of columns (width), must be <= 26
NUM_PLAYERS = 2          # supported range: 2..5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4           # number of checkers in a row needed to win

# ----- Validation of constants -----
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]


# ----- Utility functions -----
def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    # Top border
    print("+" + "---+" * cols)
    # Rows (from top to bottom)
    for r in range(rows):
        row_cells = "|"
        for c in range(cols):
            row_cells += f" {board[r][c]} |"
        print(row_cells)
        print("+" + "---+" * cols)


def col_letter_to_index(letter):
    letter = letter.strip().upper()
    if len(letter) != 1:
        return None
    if letter < "A" or letter > chr(ord("A") + COLS - 1):
        return None
    return ord(letter) - ord("A")


def get_valid_column_input():
    # Keep asking until a valid column letter is given
    while True:
        user_in = input().strip().upper()
        idx = col_letter_to_index(user_in)
        if idx is not None:
            return idx
        else:
            print("Invalid input. Please enter a valid column letter:", end=" ")


def find_row_for_col(board, col):
    # Return the row index (from bottom) where the checker should land, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, checker):
    row = find_row_for_col(board, col)
    if row is None:
        return False
    board[row][col] = checker
    return True


def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def has_won(board, checker):
    rows = len(board)
    cols = len(board[0])
    L = WIN_LENGTH

    # Horizontal
    for r in range(rows):
        for c in range(cols - L + 1):
            if all(board[r][c + k] == checker for k in range(L)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - L + 1):
            if all(board[r + k][c] == checker for k in range(L)):
                return True

    # Diagonal down-right (\)
    for r in range(rows - L + 1):
        for c in range(cols - L + 1):
            if all(board[r + k][c + k] == checker for k in range(L)):
                return True

    # Diagonal up-right (/)
    for r in range(L - 1, rows):
        for c in range(cols - L + 1):
            if all(board[r - k][c + k] == checker for k in range(L)):
                return True

    return False


def game_loop():
    board = create_board(ROWS, COLS)
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        current_player = PLAYERS[current_idx]
        print(f"Player {current_player}, please enter a column:", end=" ")

        col = get_valid_column_input()

        moved = place_checker(board, col, current_player)

        clear_screen()
        print_board(board)

        if not moved:
            # Column full, turn lost
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {current_player} loses the turn.")
            # Move to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Check for win
        if has_won(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    # Start the game
    # Show initial empty board and randomly select first player in game_loop
    game_loop()
