import os
import random
import sys

# -------------------- Configuration (change for testing only) --------------------
ROWS = 6
COLS = 7            # Max 26 (A..Z)
NUM_PLAYERS = 2     # Between 2 and 5 inclusive

TOKENS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4
# --------------------------------------------------------------------------------

def clear_screen():
    # As per assignment requirement
    os.system('clear')

def validate_settings():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # 'A' .. up to number of columns
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board, labels):
    clear_screen()
    # Header
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    print("+" + ("---+" * len(labels)))
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(board[r][c] if board[r][c] != " " else " ")
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * len(labels)))

def get_valid_column_input(labels):
    # Keep asking until a syntactically valid column letter is provided.
    # Invalid input does NOT cost the turn.
    while True:
        user_in = input().strip()
        if not user_in:
            print("Invalid input. Please enter a column letter (e.g., A).")
            continue
        ch = user_in.upper()
        if len(ch) != 1 or ch < 'A' or ch > 'Z':
            print("Invalid input. Please enter a column letter (e.g., A).")
            continue
        if ch not in labels:
            print("Invalid column. Please choose a column between {} and {}.".format(labels[0], labels[-1]))
            continue
        return ch

def place_checker(board, col_index, token):
    # Place in the lowest available row of the given column.
    # Returns True if placed, False if column full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = token
            return True
    return False  # Column is full

def check_direction(board, start_r, start_c, dr, dc, token):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    for _ in range(WIN_LEN):
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        else:
            break
    return count == WIN_LEN

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, token):
                    return True
    return False

def board_full(board):
    # If top row has no spaces, board is full because pieces stack from bottom.
    return all(cell != " " for cell in board[0])

def main():
    validate_settings()

    labels = column_labels(COLS)
    tokens_in_game = TOKENS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly pick starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board before the game starts
    print_board(board, labels)
    print(f"Player {tokens_in_game[current_player_idx]}, please enter a column:")

    while True:
        # Read and validate input (only syntax and bounds; full column loses turn later)
        col_label = get_valid_column_input(labels)
        col_index = ord(col_label) - ord('A')

        token = tokens_in_game[current_player_idx]

        # Attempt to place checker
        placed = place_checker(board, col_index, token)

        # After every turn (even if invalid due to full column), reprint board
        print_board(board, labels)

        if not placed:
            # Full column: turn is invalid and player loses the turn (no re-input)
            print(f"Column {col_label} is full. {token}'s turn is lost.")
        else:
            # Check for win
            if check_win(board, token):
                print(f"Player {token} won!")
                break
            # Check for draw
            if board_full(board):
                print("Game is a draw.")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print(f"Player {tokens_in_game[current_player_idx]}, please enter a column:")

if __name__ == "__main__":
    main()
