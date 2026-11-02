import os
import random
import sys
from typing import List, Optional, Tuple

# ----------------------------
# Configuration (constants)
# ----------------------------
ROWS = 6
COLS = 7          # Max 26 (A-Z)
NUM_PLAYERS = 2   # Between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4    # Always 4 per assignment

# ----------------------------
# Validation of configuration
# ----------------------------
def validate_config():
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if COLS < 1 or COLS > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if ROWS < 1:
        raise ValueError("ROWS must be at least 1.")
    if len(TOKENS) < NUM_PLAYERS:
        raise ValueError("Not enough tokens defined for the number of players.")


# ----------------------------
# Board utilities
# ----------------------------
Board = List[List[str]]

def create_board(rows: int, cols: int) -> Board:
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Per assignment requirement
    os.system('clear')

def column_labels(cols: int) -> List[str]:
    # Labels A, B, C, ...
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board: Board):
    cols = len(board[0])
    rows = len(board)
    labels = column_labels(cols)

    # Header
    header = "  " + "   ".join(labels)
    print(header)
    print("+---" * cols + "+")
    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            cell = board[r][c]
            row_cells.append(f"| {cell} ")
        print("".join(row_cells) + "|")
        print("+---" * cols + "+")


# ----------------------------
# Input handling
# ----------------------------
def get_valid_column_input(cols: int, prompt: str = "") -> int:
    labels = column_labels(cols)
    label_set = set(labels)
    while True:
        if prompt:
            user_in = input(prompt)
        else:
            user_in = input()
        user_in = user_in.strip().upper()
        if len(user_in) != 1 or not user_in.isalpha():
            print("Invalid input. Please enter a single uppercase letter (A-Z).")
            continue
        if user_in not in label_set:
            print(f"Invalid column. Please choose between {labels[0]} and {labels[-1]}.")
            continue
        return ord(user_in) - ord('A')


# ----------------------------
# Game mechanics
# ----------------------------
def drop_token(board: Board, col: int, token: str) -> Optional[Tuple[int, int]]:
    # Place token in lowest available row in the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None  # Column full

def is_draw(board: Board) -> bool:
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols

def check_win(board: Board, token: str) -> bool:
    rows = len(board)
    cols = len(board[0])
    need = WIN_LENGTH

    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < need and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= need:
                    return True
    return False


# ----------------------------
# Main game loop
# ----------------------------
def main():
    validate_config()

    rows, cols = ROWS, COLS
    players = TOKENS[:NUM_PLAYERS]
    board = create_board(rows, cols)

    # Randomly select starting player
    current_idx = random.randrange(NUM_PLAYERS)

    status_message = ""

    while True:
        clear_screen()
        print_board(board)
        if status_message:
            print(status_message)
            status_message = ""

        current_token = players[current_idx]
        prompt = f"Player {current_token}, please enter a column: "

        # Get valid column letter (input validation). Does not consider fullness here.
        col = get_valid_column_input(cols, prompt)

        # Try to drop token. If column full, player loses the turn.
        pos = drop_token(board, col, current_token)
        if pos is None:
            # Turn is invalid and the player loses the turn
            label = chr(ord('A') + col)
            status_message = f"Column {label} is full. Player {current_token} loses the turn."
            # Advance to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
