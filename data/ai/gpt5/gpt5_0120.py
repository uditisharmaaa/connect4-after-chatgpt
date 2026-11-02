import os
import random
import string
import sys

# Constants (submission must use 6 rows x 7 cols and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5

TOKENS = ["X", "O", "V", "H", "M"]  # in order

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    # Header
    print("  " + "   ".join(letters))
    # Horizontal line template
    hline = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(hline)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(hline)

def col_letter_to_index(s):
    if len(s) != 1:
        return None
    ch = s.upper()
    if 'A' <= ch <= 'Z':
        idx = ord(ch) - ord('A')
        return idx
    return None

def place_checker(board, col_idx, token):
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = token
            return r
    return None  # column full

def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def check_win(board, r, c, token):
    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]
    for dr, dc in directions:
        count = 1  # include the placed token
        # forward
        rr, cc = r + dr, c + dc
        while in_bounds(board, rr, cc) and board[rr][cc] == token:
            count += 1
            rr += dr
            cc += dc
        # backward
        rr, cc = r - dr, c - dc
        while in_bounds(board, rr, cc) and board[rr][cc] == token:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def get_valid_column_input(cols, current_token):
    letters = string.ascii_uppercase[:cols]
    while True:
        try:
            user_in = input(f"Player {current_token}, please enter a column: ").strip().upper()
        except EOFError:
            # If input stream closes, exit gracefully
            print()
            sys.exit(0)
        idx = col_letter_to_index(user_in)
        if idx is None or not (0 <= idx < cols):
            print(f"Invalid input. Please enter a letter between A and {letters[-1]}.")
            continue
        return idx, user_in

def validate_constants():
    ok = True
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        ok = False
    if not (1 <= ROWS):
        print("ROWS must be positive.")
        ok = False
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        ok = False
    if ok is False:
        sys.exit(1)

def main():
    validate_constants()
    board = create_board(ROWS, COLS)
    player_tokens = TOKENS[:NUM_PLAYERS]
    current_player = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_token = player_tokens[current_player]
        # Prompt for input (validate characters/range)
        col_idx, col_letter = get_valid_column_input(COLS, current_token)

        # Attempt to place checker
        row_placed = place_checker(board, col_idx, current_token)

        if row_placed is None:
            # Column is full -> invalid turn, player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {col_letter} is full. Player {current_token} loses the turn.")
            # Check draw even after a lost turn (board may already be full)
            if board_full(board):
                print("Game is a draw.")
                break
            # Next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Successful placement: show updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row_placed, col_idx, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if board_full(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
