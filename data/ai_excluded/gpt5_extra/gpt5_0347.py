import os
import random
import string
from typing import List, Optional, Tuple

# =======================
# Configuration constants
# =======================
ROWS = 6
COLS = 7           # Max 26 (A-Z)
NUM_PLAYERS = 2    # Supported: 2..5

# Player checkers in order. First NUM_PLAYERS are used.
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of consecutive checkers needed to win (fixed to 4 per assignment)
WIN_LENGTH = 4

# =======================
# Utility / Validation
# =======================
def validate_configuration(rows: int, cols: int, num_players: int) -> None:
    if cols < 1 or cols > 26:
        raise ValueError("Number of columns must be between 1 and 26.")
    if rows < 1:
        raise ValueError("Number of rows must be at least 1.")
    if num_players < 2 or num_players > 5:
        raise ValueError("Number of players must be between 2 and 5.")
    if len(CHECKERS) < num_players:
        raise ValueError("Not enough checker symbols defined for the number of players.")

# =======================
# Board management
# =======================
Board = List[List[str]]

def create_board(rows: int, cols: int) -> Board:
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen() -> None:
    # As required by the assignment: use 'clear' to refresh the terminal.
    os.system('clear')

def print_board(board: Board, col_labels: List[str]) -> None:
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header line with column letters
    header = "  " + "   ".join(col_labels)
    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)

def column_labels(cols: int) -> List[str]:
    return list(string.ascii_uppercase[:cols])

def find_lowest_empty_row(board: Board, col: int) -> Optional[int]:
    # Returns the index of the lowest empty row in the given column, or None if the column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board: Board, col: int, checker: str) -> Optional[Tuple[int, int]]:
    """
    Attempts to place a checker into the given column.
    Returns (row, col) if placed, or None if the column is full.
    """
    row_index = find_lowest_empty_row(board, col)
    if row_index is None:
        return None
    board[row_index][col] = checker
    return (row_index, col)

# =======================
# Win / Draw detection
# =======================
def check_direction(board: Board, start_r: int, start_c: int, dr: int, dc: int, checker: str) -> bool:
    """
    Check WIN_LENGTH in a row from (start_r, start_c) moving by (dr, dc).
    """
    rows = len(board)
    cols = len(board[0])
    for i in range(WIN_LENGTH):
        r = start_r + dr * i
        c = start_c + dc * i
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != checker:
            return False
    return True

def check_win(board: Board, checker: str) -> bool:
    """
    Check for a win for the given checker in any direction.
    """
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, down-right, up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, checker):
                    return True
    return False

def check_draw(board: Board) -> bool:
    # Draw if no empty cells remain
    for row in board:
        if any(cell == " " for cell in row):
            return False
    return True

# =======================
# Input handling
# =======================
def prompt_for_column(current_checker: str, valid_labels: List[str]) -> int:
    """
    Prompt the user for a column letter. Repeat until a valid letter (within the board) is given.
    Returns the column index corresponding to the valid letter.
    """
    label_set = set(valid_labels)
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        col_label = user_input.upper()
        if col_label not in label_set:
            print("Invalid column. Please choose a letter shown at the top of the board.")
            continue
        return valid_labels.index(col_label)

# =======================
# Game loop
# =======================
def main() -> None:
    validate_configuration(ROWS, COLS, NUM_PLAYERS)

    players = CHECKERS[:NUM_PLAYERS]
    labels = column_labels(COLS)
    board = create_board(ROWS, COLS)

    # Randomly select the first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board before the first move
    clear_screen()
    print_board(board, labels)

    winner: Optional[str] = None
    game_over = False

    while not game_over:
        current_checker = players[current_player_idx]

        # Prompt for a valid column letter
        col = prompt_for_column(current_checker, labels)

        # Attempt to place checker
        placement = place_checker(board, col, current_checker)
        if placement is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board, labels)
            print(f"Column {labels[col]} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move: refresh, show board, and check game state
        clear_screen()
        print_board(board, labels)

        # Check for a win
        if check_win(board, current_checker):
            winner = current_checker
            print(f"Player {winner} won!")
            game_over = True
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
