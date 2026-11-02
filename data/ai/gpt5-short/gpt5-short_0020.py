import os
import random
import sys

# =======================
# Configuration constants
# =======================
ROWS = 6
COLS = 7
WIN_LEN = 4

# Number of players (2 to 5)
NUM_PLAYERS = 2

# Symbols in play order; only the first NUM_PLAYERS are used
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# =======================
# Utility and game logic
# =======================

def clear_screen():
    # Use 'clear' as requested; fallback to 'cls' on Windows if needed.
    if os.system('clear') != 0:
        os.system('cls')

def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def column_labels(cols=COLS):
    # Labels A, B, C, ...
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board):
    labels = column_labels(len(board[0]))
    print('  ' + '   '.join(labels))
    print('+' + '---+' * len(labels))
    for r in range(len(board)):
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
        print('+' + '---+' * len(labels))

def get_active_symbols():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print(f"NUM_PLAYERS must be between 2 and 5, got {NUM_PLAYERS}.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print("Not enough symbols in PLAYER_SYMBOLS for NUM_PLAYERS.")
        sys.exit(1)
    return PLAYER_SYMBOLS[:NUM_PLAYERS]

def label_to_col(label):
    label = label.strip().upper()
    labels = column_labels(COLS)
    if label in labels:
        return labels.index(label)
    return None

def find_drop_row(board, col):
    # Return the row index where the piece will land, or None if column is full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_direction(board, start_r, start_c, dr, dc, symbol):
    # Count contiguous pieces of the same symbol starting from (start_r, start_c)
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, r, c, symbol):
    # Check all directions for 4 in a row through (r, c)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        # Count both directions minus 1 to avoid double-counting the origin
        total = (
            count_direction(board, r, c, dr, dc, symbol) +
            count_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= WIN_LEN:
            return True
    return False

def is_draw(board):
    # Draw if no spaces in top row (i.e., all columns are full)
    return all(board[0][c] != ' ' for c in range(COLS))

def get_move_input(current_symbol):
    while True:
        user_input = input(f"Player {current_symbol}, choose a column (A-{chr(ord('A')+COLS-1)}), or Q to quit: ").strip()
        if not user_input:
            print("Empty input. Please enter a column letter.")
            continue
        if user_input.lower() in ('q', 'quit', 'exit'):
            return 'QUIT'

        col = label_to_col(user_input)
        if col is None:
            print(f"Invalid column. Please enter a letter A-{chr(ord('A')+COLS-1)}.")
            continue

        return col

def drop_piece(board, col, symbol):
    row = find_drop_row(board, col)
    if row is None:
        return None  # Column full
    board[row][col] = symbol
    return row

def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def random_first_player(num_players):
    return random.randrange(num_players)

def game_loop():
    active_symbols = get_active_symbols()
    board = create_board()
    current_idx = random_first_player(len(active_symbols))

    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {' '.join(active_symbols)}  |  Turn: {active_symbols[current_idx]}")
        print_board(board)

        move = get_move_input(active_symbols[current_idx])
        if move == 'QUIT':
            print("Game ended by user.")
            break

        col = move
        row = drop_piece(board, col, active_symbols[current_idx])
        if row is None:
            print("That column is full. Press Enter to try again.")
            input()
            continue

        # Check for win
        if is_winning_move(board, row, col, active_symbols[current_idx]):
            clear_screen()
            print_board(board)
            print(f"Player {active_symbols[current_idx]} wins!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = next_player_index(current_idx, len(active_symbols))

def main():
    random.seed()  # Seed from system time or OS entropy
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted.")

if __name__ == "__main__":
    main()
