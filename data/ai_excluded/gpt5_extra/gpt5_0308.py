import os
import random
import string
import sys

# --------- Configuration (feel free to change for testing) ----------
ROWS = 6
COLS = 7            # Max 26
NUM_PLAYERS = 2     # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
# --------------------------------------------------------------------

def clear_screen():
    # As per assignment requirement
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)
    # Grid
    horiz = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(horiz)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(horiz)

def is_valid_column_letter(ch, cols):
    if len(ch) != 1:
        return False
    if ch not in string.ascii_uppercase:
        return False
    idx = ord(ch) - ord('A')
    return 0 <= idx < cols

def get_column_index_from_input(prompt, cols):
    while True:
        user_in = input(prompt).strip()
        if user_in == "":
            print("Invalid input. Please enter a column letter.")
            continue
        ch = user_in.upper()
        if not is_valid_column_letter(ch, cols):
            print("Invalid column. Please enter a valid column letter.")
            continue
        return ord(ch) - ord('A')

def place_checker(board, col, checker):
    """
    Places the checker in the lowest available spot in the given column.
    Returns the row index where it was placed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full

def check_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r = start_r
    c = start_c
    for _ in range(WIN_LENGTH):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != checker:
            return False
        r += dr
        c += dc
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, checker):
                    return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def build_players(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    return CHECKERS[:num_players]

def validate_config():
    if COLS > 26:
        raise ValueError("COLS must be at most 26 (A-Z).")
    if ROWS <= 0 or COLS <= 0:
        raise ValueError("ROWS and COLS must be positive integers.")

def main():
    validate_config()
    players = build_players(NUM_PLAYERS)
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_idx = random.randrange(len(players))

    # Show initial empty board
    print_board(board)

    winner = None
    while True:
        current_player = players[current_idx]
        print(f"Player {current_player}, please enter a column:")
        col = get_column_index_from_input("> ", COLS)

        # Attempt to place
        placed_row = place_checker(board, col, current_player)
        if placed_row is None:
            # Column full: lose the turn
            print("Column is full. Turn lost.")
            # Show the board again for clarity (no change)
            print_board(board)
            # Next player
            current_idx = (current_idx + 1) % len(players)
            continue

        # After placement, check for win or draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            winner = current_player
            break

        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        print_board(board)
        current_idx = (current_idx + 1) % len(players)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
