import os
import random

# ----- Configuration constants -----
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"

# Choose how many players are playing (between 2 and 5)
NUM_PLAYERS = 2  # change to 3, 4, or 5 if desired

# Player symbols in turn order. Only the first NUM_PLAYERS are used.
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# ----- Utility functions -----
def clear_screen():
    # Use the command requested
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Column labels
    print("  " + " ".join(COL_LABELS))
    # Rows
    for r in range(ROWS):
        row_str = [board[r][c] for c in range(COLS)]
        print(str(ROWS - r) + " " + " ".join(row_str))
    # Bottom line for clarity
    print()

def col_from_label(label):
    label = label.upper()
    if label in COL_LABELS:
        return COL_LABELS.index(label)
    return None

def is_column_full(board, col):
    return board[0][col] != ' '

def get_move(board, player_symbol):
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").strip().upper()
        if len(move) != 1:
            print("Please enter a single letter from A to G.")
            continue
        col = col_from_label(move)
        if col is None:
            print("Invalid column. Please enter a letter from A to G.")
            continue
        if is_column_full(board, col):
            print("That column is full. Choose another column.")
            continue
        return col

def apply_move(board, col, player_symbol):
    # Drop from bottom up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player_symbol
            return r, col
    # Should not reach here due to validation
    return None, None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_winner(board, last_r, last_c):
    if last_r is None or last_c is None:
        return False
    symbol = board[last_r][last_c]
    if symbol == ' ':
        return False

    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right / up-left
        (1, -1),  # Diagonal down-left / up-right
    ]

    for dr, dc in directions:
        # Count both directions from the last placed piece, minus one to avoid double-counting the center
        total = (
            count_in_direction(board, last_r, last_c, dr, dc, symbol) +
            count_in_direction(board, last_r, last_c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False

def is_draw(board):
    # Draw if no spaces in the top row
    return all(board[0][c] != ' ' for c in range(COLS))

# ----- Game loop -----
def main():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()

    current_player_idx = random.randrange(NUM_PLAYERS)
    winner_symbol = None

    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {' '.join(symbols)}")
        print_board(board)

        player_symbol = symbols[current_player_idx]
        col = get_move(board, player_symbol)
        r, c = apply_move(board, col, player_symbol)

        if check_winner(board, r, c):
            winner_symbol = player_symbol
            clear_screen()
            print_board(board)
            print(f"Player {winner_symbol} wins!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
