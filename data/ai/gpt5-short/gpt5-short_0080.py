Here’s a simple, readable Connect 4 implementation that meets your requirements.

- 6 rows x 7 columns
- Columns labeled A–G
- 2 to 5 players (X, O, V, H, M) controlled by a constant
- Random first player
- Input validation
- Win and draw detection
- Uses os.system('clear') to refresh the screen

Copy this into a .py file and run it.

import os
import random
import sys

# Constants you can tweak
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
ALL_PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set between 2 and 5

def clear_screen():
    # Uses the requested clear command
    os.system('clear')

def make_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, active_players, current_player_idx):
    clear_screen()
    # Column header
    print('  ' + ' '.join(COLUMN_LABELS))
    # Rows
    for r in range(ROWS):
        print(str(ROWS - r) + ' ' + ' '.join(board[r]))
    # Footer line for clarity
    print('  ' + '-'.join(COLUMN_LABELS))
    # Status line
    current_symbol = active_players[current_player_idx]
    print(f"Players: {', '.join(active_players)}  |  Current: {current_symbol}")

def find_drop_row(board, col):
    # Return the bottom-most empty row index in given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr, cc = r + dr, c + dc
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def is_winning_move(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1  # include the placed piece
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def is_draw(board):
    # Draw if no spaces in top row
    return all(board[0][c] != ' ' for c in range(COLS))

def get_valid_column_input(prompt):
    while True:
        raw = input(prompt).strip().upper()
        if raw == '':
            print("Please enter a column letter A-G.")
            continue
        if len(raw) != 1 or raw not in COLUMN_LABELS:
            print("Invalid input. Enter a single column letter A-G.")
            continue
        return COLUMN_LABELS.index(raw)

def main():
    # Validate NUM_PLAYERS
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    active_players = ALL_PLAYERS[:NUM_PLAYERS]

    board = make_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board, active_players, current_player_idx)
        symbol = active_players[current_player_idx]

        # Input and validation loop
        while True:
            col = get_valid_column_input(f"Player {symbol}, choose a column (A-G): ")
            drop_row = find_drop_row(board, col)
            if drop_row is None:
                print("That column is full. Try another.")
                continue
            break

        # Place piece
        board[drop_row][col] = symbol

        # Check win
        if is_winning_move(board, drop_row, col, symbol):
            print_board(board, active_players, current_player_idx)
            print(f"Player {symbol} wins!")
            break

        # Check draw
        if is_draw(board):
            print_board(board, active_players, current_player_idx)
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
