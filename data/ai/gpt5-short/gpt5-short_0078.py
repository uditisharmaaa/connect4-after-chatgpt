import os
import random

# =========================
# Configurable constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must match COLS
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5 (and <= len(PLAYER_SYMBOLS))

# =========================
# Utility functions
# =========================
def clear_screen():
    # Uses the requested clear command
    os.system('clear')

def make_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Header
    print('  ' + ' '.join(COLUMN_LABELS[:len(board[0])]))
    # Rows
    for r in range(len(board)):
        row_str = []
        for c in range(len(board[0])):
            row_str.append(board[r][c] if board[r][c] != ' ' else '.')
        print(str(len(board) - r) + ' ' + ' '.join(row_str))
    print()

def get_player_symbols():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough symbols in PLAYER_SYMBOLS.")
    return PLAYER_SYMBOLS[:NUM_PLAYERS]

def get_move_input(current_symbol):
    while True:
        move = input(f"Player {current_symbol}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}): ").strip()
        if len(move) == 0:
            print("Please enter a column letter.")
            continue
        col_char = move[0].upper()
        if col_char not in COLUMN_LABELS[:COLS]:
            print(f"Invalid column. Choose between {COLUMN_LABELS[0]} and {COLUMN_LABELS[COLS-1]}.")
            continue
        col = COLUMN_LABELS.index(col_char)
        return col

def drop_piece(board, col, symbol):
    # Place piece in the lowest empty row in given column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None  # Column is full

def is_full_column(board, col):
    return board[0][col] != ' '

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        if count == 4:
            return True
        rr += dr
        cc += dc
    return False

def check_winner(board, last_r, last_c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (-1, 1),  # up-right
    ]
    for dr, dc in directions:
        # To count 4 in a row, we need to extend both ways from last move
        total = 1  # count the last placed piece
        # Extend one way
        rr, cc = last_r + dr, last_c + dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            total += 1
            rr += dr
            cc += dc
        # Extend the opposite way
        rr, cc = last_r - dr, last_c - dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            total += 1
            rr -= dr
            cc -= dc
        if total >= 4:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

# =========================
# Game loop
# =========================
def main():
    clear_screen()
    symbols = get_player_symbols()
    board = make_board(ROWS, COLS)

    # Random first player
    current_player_index = random.randrange(len(symbols))

    winner = None
    last_move = None

    while True:
        clear_screen()
        print_board(board)
        current_symbol = symbols[current_player_index]
        print(f"Current player: {current_symbol}")

        # Get a valid move
        while True:
            col = get_move_input(current_symbol)
            if is_full_column(board, col):
                print("That column is full. Try another one.")
                continue
            result = drop_piece(board, col, current_symbol)
            if result is None:
                print("That column is full. Try another one.")
                continue
            last_move = result
            break

        # Check for win
        r, c = last_move
        if check_winner(board, r, c, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins!")
            winner = current_symbol
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % len(symbols)

    # Game over
    print("Game over.")

if __name__ == "__main__":
    main()
