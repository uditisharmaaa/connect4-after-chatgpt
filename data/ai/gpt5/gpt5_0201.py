import os
import random
import string

# ==========================
# Configuration (constants)
# ==========================
ROWS = 6
COLS = 7      # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]  # In order
WIN_LENGTH = 4

# ==========================
# Validation of configuration
# ==========================
if COLS < 1 or COLS > 26:
    raise ValueError("COLS must be between 1 and 26")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1")
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5")

PLAYER_MARKS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

# ==========================
# Board utilities
# ==========================
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Top border
    print("+" + "---+" * COLS)
    # Rows
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * COLS)

def is_board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def drop_checker(board, col_index, checker):
    # Place checker in the lowest available row in the given column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return None  # Column full

def check_win(board, checker):
    # Check horizontal, vertical, and both diagonals for WIN_LENGTH in a row
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue

            # Horizontal right
            if c + WIN_LENGTH - 1 < COLS:
                ok = True
                for k in range(WIN_LENGTH):
                    if board[r][c + k] != checker:
                        ok = False
                        break
                if ok:
                    return True

            # Vertical down
            if r + WIN_LENGTH - 1 < ROWS:
                ok = True
                for k in range(WIN_LENGTH):
                    if board[r + k][c] != checker:
                        ok = False
                        break
                if ok:
                    return True

            # Diagonal down-right
            if r + WIN_LENGTH - 1 < ROWS and c + WIN_LENGTH - 1 < COLS:
                ok = True
                for k in range(WIN_LENGTH):
                    if board[r + k][c + k] != checker:
                        ok = False
                        break
                if ok:
                    return True

            # Diagonal up-right
            if r - (WIN_LENGTH - 1) >= 0 and c + WIN_LENGTH - 1 < COLS:
                ok = True
                for k in range(WIN_LENGTH):
                    if board[r - k][c + k] != checker:
                        ok = False
                        break
                if ok:
                    return True

    return False

def get_valid_column_input():
    # Keep asking until the user enters a single uppercase letter within range
    while True:
        user_input = input("Please enter a column: ").strip()
        if len(user_input) != 1:
            print("Invalid input. Enter a single uppercase letter for the column.")
            continue
        ch = user_input.upper()
        if ch not in COLUMN_LABELS:
            print("Invalid column. Valid columns are:", " ".join(COLUMN_LABELS))
            continue
        return ch

# ==========================
# Game loop
# ==========================
def main():
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    print_board(board)

    while True:
        current_checker = PLAYER_MARKS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        col_label = get_valid_column_input()
        col_index = COLUMN_LABELS.index(col_label)

        # Attempt to drop the checker
        result = drop_checker(board, col_index, current_checker)
        if result is None:
            # Column full: lose the turn
            print_board(board)
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Continue to next loop after showing updated board with message
            continue

        # Checker placed; print board and check for win/draw
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
