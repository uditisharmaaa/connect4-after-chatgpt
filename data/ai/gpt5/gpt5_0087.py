import os
import random
import time
import string
from typing import List, Optional, Tuple

# -------------------------
# Configuration (Constants)
# -------------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Supports 2 to 5
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 in a row to win

# Validate configuration
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert COLS <= 26, "Maximum of 26 columns supported (A-Z)."
PLAYERS = TOKENS[:NUM_PLAYERS]


# -------------------------
# Utility and Game Functions
# -------------------------
def clear_screen() -> None:
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]

    # Column headers
    print("  " + "   ".join(letters))
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))


def get_valid_column_input(valid_cols: int, prompt: str) -> str:
    letters = string.ascii_uppercase[:valid_cols]
    valid_set = set(letters)
    while True:
        inp = input(prompt).strip()
        if len(inp) != 1:
            # invalid length input
            continue
        ch = inp.upper()
        if ch in valid_set:
            return ch
        # Not a valid column letter; retry


def column_is_full(board: List[List[str]], col: int) -> bool:
    return board[0][col] != " "


def place_checker(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    # Place in the lowest available row in the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None  # Column full (should be checked beforehand)


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win(board: List[List[str]], token: str) -> bool:
    rows = len(board)
    cols = len(board[0])
    L = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                end_r = r + (L - 1) * dr
                end_c = c + (L - 1) * dc
                if not in_bounds(end_r, end_c, rows, cols):
                    continue
                win = True
                for k in range(L):
                    rr = r + k * dr
                    cc = c + k * dc
                    if board[rr][cc] != token:
                        win = False
                        break
                if win:
                    return True
    return False


def check_draw(board: List[List[str]]) -> bool:
    # Draw if top row has no spaces (board is full)
    return all(cell != " " for cell in board[0])


# -------------------------
# Main Game Loop
# -------------------------
def main() -> None:
    board = create_board(ROWS, COLS)
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial screen
    clear_screen()
    print_board(board)

    while True:
        player_token = PLAYERS[current_idx]
        # Prompt
        prompt = f"Player {player_token}, please enter a column: "
        col_letter = get_valid_column_input(COLS, prompt)
        col_index = ord(col_letter) - ord('A')

        # Handle full column -> lose turn
        if column_is_full(board, col_index):
            clear_screen()
            print_board(board)
            print(f"Column {col_letter} is full. Player {player_token} loses the turn.")
            time.sleep(1.5)
            # Next player's turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        place_checker(board, col_index, player_token)

        # After move: clear and print updated board
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, player_token):
            print(f"Player {player_token} won!")
            break

        # Check draw
        if check_draw(board):
            print("It's a draw.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
