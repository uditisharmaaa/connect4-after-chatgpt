import os
import random
import sys

# ----- Configuration constants -----
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Available player tokens in order; use the first NUM_PLAYERS of these
TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set between 2 and 5

# ----- Utility functions -----
def clear_screen():
    os.system('clear')  # per requirement; on Windows you may use 'cls'

def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS[:COLS]))
    for r in range(ROWS):
        print("| " + " ".join(board[r]) + " |")
    print("+" + "-" * (2 * COLS - 1) + "+")

def is_valid_column(board, col_index):
    if col_index < 0 or col_index >= COLS:
        return False
    # Column is valid if the top cell is empty
    return board[0][col_index] == ' '

def get_next_open_row(board, col_index):
    # Returns the row index (bottom-most free spot) in the given column or None
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            return r
    return None

def drop_piece(board, row, col, token):
    board[row][col] = token

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, token):
    # Check horizontal (right)
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == token and
                board[r][c + 1] == token and
                board[r][c + 2] == token and
                board[r][c + 3] == token):
                return True

    # Check vertical (down)
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (board[r][c] == token and
                board[r + 1][c] == token and
                board[r + 2][c] == token and
                board[r + 3][c] == token):
                return True

    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == token and
                board[r + 1][c + 1] == token and
                board[r + 2][c + 2] == token and
                board[r + 3][c + 3] == token):
                return True

    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == token and
                board[r - 1][c + 1] == token and
                board[r - 2][c + 2] == token and
                board[r - 3][c + 3] == token):
                return True

    return False

def check_draw(board):
    # Draw if no spaces in the top row (i.e., all columns filled)
    return all(cell != ' ' for cell in board[0])

def parse_column_input(user_input):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    if user_input not in COLUMN_LABELS[:COLS]:
        return None
    return COLUMN_LABELS.index(user_input)

def get_player_move(board, token):
    while True:
        raw = input(f"Player {token}, choose a column ({COLUMN_LABELS[:COLS]}): ")
        col_index = parse_column_input(raw)
        if col_index is None:
            print(f"Invalid input. Please enter one letter from {COLUMN_LABELS[:COLS]}.")
            continue
        if not is_valid_column(board, col_index):
            print("That column is full. Try another one.")
            continue
        return col_index

def next_player_index(current_idx, num_players):
    return (current_idx + 1) % num_players

def validate_config():
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(TOKENS):
        print("Error: Not enough tokens defined for the requested number of players.")
        sys.exit(1)

# ----- Game loop -----
def main():
    validate_config()
    players = TOKENS[:NUM_PLAYERS]
    board = create_board()

    current_idx = random.randrange(NUM_PLAYERS)  # random first player
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Players: {' '.join(players)}")
    print(f"First player (random): {players[current_idx]}\n")
    print_board(board)

    while True:
        token = players[current_idx]
        col = get_player_move(board, token)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, token)

        clear_screen()
        print_board(board)

        if check_win(board, token):
            print(f"Player {token} wins!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_idx = next_player_index(current_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
