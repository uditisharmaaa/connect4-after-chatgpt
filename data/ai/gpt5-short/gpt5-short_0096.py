import os
import random
import sys

# =========================
# Configuration (edit here)
# =========================
NUM_ROWS = 6
NUM_COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Set number of players (2 to 5)
NUM_PLAYERS = 2  # change to 3, 4, or 5 if desired

# Player symbols in turn order (use first NUM_PLAYERS of this list)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
# =========================

def clear_screen():
    # As requested
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Column labels
    print('  ' + ' '.join(COLUMN_LABELS[:len(board[0])]))
    # Rows
    for r in range(len(board)):
        print(str(len(board) - r) + ' ' + ' '.join(board[r]))
    print()

def letter_to_col(letter):
    letter = letter.upper()
    if letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(letter)
    return None

def find_drop_row(board, col):
    # Returns the row index where a piece would drop in the given column,
    # or None if the column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    rows, cols = len(board), len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, last_r, last_c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def is_draw(board):
    # Draw if all top cells are filled
    return all(cell != ' ' for cell in board[0])

def get_valid_move(board, current_symbol):
    while True:
        move = input(f"Player {current_symbol}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[len(board[0])-1]}): ").strip()
        if len(move) != 1:
            print("Please type a single letter for the column.")
            continue
        col = letter_to_col(move)
        if col is None or col >= len(board[0]):
            print("Invalid column. Try again.")
            continue
        drop_row = find_drop_row(board, col)
        if drop_row is None:
            print("That column is full. Pick another.")
            continue
        return col, drop_row

def main():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print("Not enough player symbols for the chosen NUM_PLAYERS.")
        sys.exit(1)

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    board = create_board(NUM_ROWS, NUM_COLS)

    # Random first player
    current_index = random.randrange(NUM_PLAYERS)

    while True:
        print_board(board)
        print("Players in order:", ' '.join(symbols))
        print(f"Starting player this game: {symbols[current_index]}")
        break

    # Main game loop
    while True:
        current_symbol = symbols[current_index]
        print_board(board)
        print("Players in order:", ' '.join(symbols))
        print(f"Current turn: {current_symbol}")

        col, row = get_valid_move(board, current_symbol)
        board[row][col] = current_symbol

        # Check for win
        if is_winning_move(board, row, col, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
