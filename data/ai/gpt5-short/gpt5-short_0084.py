import os
import random
import sys

# ====== Configuration constants ======
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # Must match COLS
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']        # Up to 5 players
NUM_PLAYERS = 2                                   # Set between 2 and 5 inclusive

# ====== Utility functions ======
def clear_screen():
    # Clear terminal screen
    os.system('clear')  # On Windows, you can change to 'cls' if needed

def create_board(rows, cols):
    return [['.' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    print('  ' + ' '.join(COL_LABELS))
    # Print each row
    for r in range(ROWS):
        print(str(ROWS - r) + ' ' + ' '.join(board[r]))
    print()

def get_column_index_from_label(label):
    label = label.upper()
    if label in COL_LABELS:
        return COL_LABELS.index(label)
    return None

def is_valid_player_count(n):
    return 2 <= n <= len(PLAYER_SYMBOLS)

def drop_piece(board, col, symbol):
    # Drop into lowest available row in column; return row index or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = symbol
            return r
    return None

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

def check_win(board, r, c, symbol):
    # Check four directions (pairs): horizontal, vertical, diag1, diag2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count both ways from the last placed piece
        total = (
            count_in_direction(board, r, c, dr, dc, symbol) +
            count_in_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False

def check_draw(board):
    # Draw if top row has no empty cells
    return all(cell != '.' for cell in board[0])

def next_player_index(idx, num_players):
    return (idx + 1) % num_players

def get_move_input(current_symbol):
    while True:
        move = input(f"Player {current_symbol}, choose a column (A-G) or Q to quit: ").strip().upper()
        if move == 'Q':
            return 'Q'
        col_idx = get_column_index_from_label(move)
        if col_idx is None:
            print("Invalid column. Please enter a letter A-G.")
            continue
        return col_idx

# ====== Game loop ======
def play_game():
    # Validate configuration
    if COLS != len(COL_LABELS):
        print("Configuration error: COLS must match length of COL_LABELS.")
        sys.exit(1)
    if not is_valid_player_count(NUM_PLAYERS):
        print(f"Configuration error: NUM_PLAYERS must be between 2 and {len(PLAYER_SYMBOLS)}.")
        sys.exit(1)

    active_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    current_idx = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        current_symbol = active_symbols[current_idx]

        user_input = get_move_input(current_symbol)
        if user_input == 'Q':
            print("Game aborted. Goodbye!")
            return

        col = user_input

        # Attempt to drop piece
        dropped_row = drop_piece(board, col, current_symbol)
        if dropped_row is None:
            print("That column is full. Press Enter to choose another column.")
            input()
            continue

        # Check for win
        if check_win(board, dropped_row, col, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves available.")
            break

        # Next player's turn
        current_idx = next_player_index(current_idx, NUM_PLAYERS)

def main():
    play_game()

if __name__ == "__main__":
    main()
