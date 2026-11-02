import os
import random
import sys

# ----------------- Configuration Constants -----------------
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A'..'G']

# Allowed player symbols in the order they will be used
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Set number of players here (between 2 and 5 inclusive)
NUM_PLAYERS = 2  # Change to 3, 4, or 5 as needed

# -----------------------------------------------------------

def clear_screen():
    # Uses 'clear' as requested
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print rows top to bottom
    for r in range(ROWS):
        row_cells = [board[r][c] for c in range(COLS)]
        print(str(ROWS - r) + ' ' + ' '.join(row_cells))
    # Bottom line for aesthetics
    print()

def drop_piece(board, col, symbol):
    """
    Attempt to drop a piece into column 'col' (0-based).
    Returns (row_index, col_index) if successful, or None if column is full.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return (r, col)
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count consecutive 'symbol' cells starting at (start_r, start_c) and
    moving step (dr, dc) NOT including the starting cell.
    """
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, last_r, last_c, symbol):
    """
    Check if placing 'symbol' at (last_r, last_c) created a connect-4.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # count the last placed piece
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def is_draw(board):
    # Draw if no spaces left in the top row
    return all(board[0][c] != ' ' for c in range(COLS))

def get_valid_column_input(prompt):
    """
    Prompt user for a column letter A-G (case-insensitive).
    Returns the 0-based column index, or None if user wants to quit.
    """
    while True:
        user_input = input(prompt).strip().upper()
        if user_input == '':
            print("Please enter a column letter (A-G).")
            continue
        if user_input == 'Q':
            return None
        if len(user_input) != 1 or user_input < 'A' or user_input > chr(ord('A') + COLS - 1):
            print(f"Invalid input. Enter a column letter between A and {COLUMN_LABELS[-1]}, or Q to quit.")
            continue
        return ord(user_input) - ord('A')

def show_header(players, current_idx):
    print("Connect 4 - Intro CS Edition")
    print(f"Players: {' '.join(players)}")
    print(f"Current turn: {players[current_idx]}")
    print("Enter A-G to drop a piece, or Q to quit.")
    print()

def main():
    # Validate NUM_PLAYERS
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()

    # Randomly choose first player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        show_header(players, current_idx)
        print_board(board)

        col = get_valid_column_input(f"Player {players[current_idx]}, choose a column (A-{COLUMN_LABELS[-1]}): ")
        if col is None:
            print("Game aborted by user.")
            break

        # Try to drop piece; if column full, prompt again
        pos = drop_piece(board, col, players[current_idx])
        if pos is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Press Enter to try a different column.")
            input()
            continue

        last_r, last_c = pos

        # Check for a win
        if is_winning_move(board, last_r, last_c, players[current_idx]):
            clear_screen()
            show_header(players, current_idx)
            print_board(board)
            print(f"Player {players[current_idx]} wins! Congratulations!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            show_header(players, current_idx)
            print_board(board)
            print("It's a draw! Board is full.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
