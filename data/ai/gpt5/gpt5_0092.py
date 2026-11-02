import os
import random
import string
import sys

# ====== Constants (adjustable, but submission requires these values) ======
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4

CHECKER_ORDER = ["X", "O", "V", "H", "M"]  # In order for 2..5 players
CHECKERS = CHECKER_ORDER[:NUM_PLAYERS]

# ====== Utility Functions ======
def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    if cols > 26:
        raise ValueError("Maximum supported columns is 26.")
    return list(string.ascii_uppercase[:cols])

def draw_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header labels
    header = "  " + "   ".join(labels)
    print(header)

    # Horizontal separator builder
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def find_drop_row(board, col_idx):
    # Return the row index where the checker will land, or None if column is full
    for r in range(len(board) - 1, -1, -1):  # bottom to top
        if board[r][col_idx] == " ":
            return r
    return None

def drop_checker(board, col_idx, checker):
    r = find_drop_row(board, col_idx)
    if r is None:
        return False
    board[r][col_idx] = checker
    return True

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    if count >= WIN_LENGTH:
                        return True
                    rr += dr
                    cc += dc
    return False

def prompt_for_column(current_checker, cols):
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        try:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        # Input validation: must be exactly one letter within labels
        if len(user_input) != 1 or user_input not in valid_set:
            print("Invalid input. Please enter a single column letter within the board (e.g., A, B, ...).")
            continue
        return labels.index(user_input)

# ====== Main Game Loop ======
def main():
    # Basic validations for constants
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if COLS > 26:
        raise ValueError("COLS must be 26 or fewer to fit A-Z labels.")
    if ROWS < 1 or COLS < 1:
        raise ValueError("Board dimensions must be positive.")

    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player = random.randrange(NUM_PLAYERS)

    # Initial board display
    draw_board(board)

    while True:
        current_checker = CHECKERS[current_player]

        # Show prompt after board
        col_idx = prompt_for_column(current_checker, COLS)

        # Attempt to drop checker
        success = drop_checker(board, col_idx, current_checker)
        draw_board(board)

        if not success:
            # Column full: turn is invalid and the player loses the turn
            col_label = column_labels(COLS)[col_idx]
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
        else:
            # Check for win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                break

        # Next player's turn (even if move was invalid due to full column)
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
