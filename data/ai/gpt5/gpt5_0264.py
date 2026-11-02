import os
import random
import string
from typing import List, Optional, Tuple

# ====== Configuration (change these constants if needed) ======
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 as per assignment
# =============================================================


def clear_screen() -> None:
    # Clear screen on Unix/Linux/macOS
    os.system('clear')


def make_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    # Labels A, B, C, ...
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    labels = column_labels(len(board[0]))
    # Header
    print("  " + "   ".join(labels))
    # Grid
    top = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(top)
        row_cells = "|".join(f" {board[r][c]} " for c in range(len(labels)))
        print(f"|{row_cells}|")
    print(top)


def get_valid_input(current_checker: str, num_cols: int) -> str:
    labels = column_labels(num_cols)
    valid_set = set(labels)
    while True:
        user = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(user) == 1 and user in valid_set:
            return user
        # Invalid input, reprompt (turn is not lost)
        print(f"Invalid input. Please enter a single letter between {labels[0]} and {labels[-1]}.")


def drop_checker(board: List[List[str]], col_idx: int, checker: str) -> Optional[Tuple[int, int]]:
    # Place in lowest available row in the given column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return (r, col_idx)
    # Column full
    return None


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win_from(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, checker: str) -> bool:
    rows, cols = len(board), len(board[0])
    for k in range(WIN_LENGTH):
        rr = start_r + dr * k
        cc = start_c + dc * k
        if not in_bounds(rr, cc, rows, cols) or board[rr][cc] != checker:
            return False
    return True


def check_win(board: List[List[str]], checker: str) -> bool:
    rows, cols = len(board), len(board[0])
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diag down-right
        (1, -1),   # diag down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                if check_win_from(board, r, c, dr, dc, checker):
                    return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    # Draw if no spaces left
    return all(cell != " " for row in board for cell in row)


def main() -> None:
    # Basic validations against constraints
    if COLS < 1 or COLS > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(CHECKERS):
        raise ValueError("Not enough checker symbols defined for the number of players.")

    players = CHECKERS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)

    # Randomly select starting player
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    winner: Optional[str] = None
    while True:
        current_checker = players[current_idx]

        # Prompt for a valid column letter
        col_letter = get_valid_input(current_checker, COLS)
        col_idx = ord(col_letter) - ord('A')

        # Attempt to drop; if column full, player loses turn
        placed = drop_checker(board, col_idx, current_checker)
        clear_screen()
        print_board(board)

        if placed is None:
            # Column full: turn is invalid and lost (no reprompt)
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
        else:
            # Check for win
            if check_win(board, current_checker):
                winner = current_checker
                print(f"Player {winner} won!")
                break

        # Check for draw after the move (or skipped move)
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

    # Game over


if __name__ == "__main__":
    main()
