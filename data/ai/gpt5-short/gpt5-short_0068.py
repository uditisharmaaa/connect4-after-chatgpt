import os
import random
import sys

# Constants you can tweak for your class/project
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A','B','C','D','E','F','G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5 to choose how many players participate

# ------------- Utility functions -------------

def clear_screen():
    # Uses 'clear' per requirement
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print each row
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('| ' + ' | '.join(row_cells) + ' |')
    print('-' * (4 * COLS + 1))

def column_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COLUMN_LABELS:
        return COLUMN_LABELS.index(s)
    return None

def next_open_row(board, col):
    # Returns the bottom-most open row index in the given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board, row, col, symbol):
    board[row][col] = symbol

def is_draw(board):
    # Draw if top row has no spaces (board full)
    return all(board[0][c] != ' ' for c in range(COLS))

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    # Count consecutive pieces including the starting cell in the given direction pair (+ and -)
    count = 1  # start cell
    # Forward direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    # Backward direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r -= dr
        c -= dc
    return count

def is_winning_move(board, last_r, last_c, symbol):
    # Check all four directions crossing the last placed piece
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horiz, vert, diag down-right, diag down-left
    for dr, dc in directions:
        if count_in_direction(board, last_r, last_c, dr, dc, symbol) >= 4:
            return True
    return False

def get_valid_move(board, current_symbol):
    while True:
        choice = input(f"Player {current_symbol}, choose a column ({'/'.join(COLUMN_LABELS)}): ").strip()
        col = column_from_input(choice)
        if col is None:
            print("Invalid input. Enter a single letter A-G corresponding to a column.")
            continue
        row = next_open_row(board, col)
        if row is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another.")
            continue
        return row, col

def validate_num_players(n):
    if not (2 <= n <= len(PLAYER_SYMBOLS)):
        print(f"NUM_PLAYERS must be between 2 and {len(PLAYER_SYMBOLS)}. Using 2 players by default.")
        return 2
    return n

# ------------- Game loop -------------

def play_game():
    n_players = validate_num_players(NUM_PLAYERS)
    symbols = PLAYER_SYMBOLS[:n_players]

    board = create_board()
    start_index = random.randrange(n_players)
    current_index = start_index

    clear_screen()
    print("Connect 4")
    print(f"Players: {', '.join(symbols)}")
    print(f"Randomly selected first player: {symbols[current_index]}\n")
    print_board(board)

    while True:
        try:
            current_symbol = symbols[current_index]
            row, col = get_valid_move(board, current_symbol)
            drop_piece(board, row, col, current_symbol)

            clear_screen()
            print_board(board)

            # Check for win
            if is_winning_move(board, row, col, current_symbol):
                print(f"Player {current_symbol} wins!")
                break

            # Check for draw
            if is_draw(board):
                print("It's a draw!")
                break

            # Next player's turn
            current_index = (current_index + 1) % n_players

        except KeyboardInterrupt:
            print("\nGame interrupted. Goodbye!")
            sys.exit(0)

def main():
    play_game()

if __name__ == "__main__":
    main()
