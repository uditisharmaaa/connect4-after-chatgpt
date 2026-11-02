import os
import random
import string

# ==== CONSTANTS ====
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # You can change this (up to 5)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
MAX_COLS = 26

# ==== FUNCTIONS ====

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create and return a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board in a user-friendly format."""
    cols = len(board[0])
    rows = len(board)

    # Print column headers (A, B, ...)
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))
    print("+" + "---+" * cols)

    for r in range(rows):
        print("|", end="")
        for c in range(cols):
            print(" {} |".format(board[r][c]), end="")
        print()
        print("+" + "---+" * cols)

def is_valid_column(col, cols):
    """Check if the column character is a valid, in-bounds column letter."""
    return col in [string.ascii_uppercase[i] for i in range(cols)]

def is_column_full(board, col_idx):
    """Return True if the top cell in the given column is not empty (column is full)."""
    return board[0][col_idx] != " "

def get_available_row(board, col_idx):
    """Return the lowest available row index in the column or None if full."""
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            return row
    return None

def drop_checker(board, col_idx, checker):
    """Place a checker in the lowest available row for the given column."""
    row_idx = get_available_row(board, col_idx)
    if row_idx is not None:
        board[row_idx][col_idx] = checker
        return row_idx
    else:
        return None  # Column full

def check_direction(board, row, col, d_row, d_col, checker):
    """Count consecutive checkers of same type starting from (row, col) in the direction (d_row, d_col)."""
    count = 0
    rows = len(board)
    cols = len(board[0])
    r, c = row, col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col
    return count

def check_for_win(board, row, col, checker):
    """Check all directions if the last move resulted in a win."""
    # Directions: (delta_row, delta_col)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for d_row, d_col in directions:
        # Negative direction
        neg_count = check_direction(board, row - d_row, col - d_col, -d_row, -d_col, checker)
        # Positive direction (including starting cell)
        pos_count = check_direction(board, row, col, d_row, d_col, checker)
        # Total in this direction
        total = neg_count + pos_count
        if total >= WIN_LENGTH:
            return True
    return False

def check_for_draw(board):
    """Return True if all cells are filled (board full) and there's no winner."""
    for row in board:
        if " " in row:
            return False
    return True

def get_player_column_input(current_player, cols):
    """Prompt the player for a valid column letter. Handle invalid input."""
    valid_cols = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in valid_cols:
            print(f"Invalid input! Please enter a letter between {valid_cols[0]} and {valid_cols[-1]}.")
            continue
        return user_input

def main():
    # Check for bounds
    if NUM_COLS > MAX_COLS or NUM_PLAYERS > len(PLAYER_CHECKERS) or NUM_PLAYERS < 2:
        print("Invalid configuration. Max columns: {}, Players: 2-{}.".format(MAX_COLS, len(PLAYER_CHECKERS)))
        return

    # Setup
    board = create_board(NUM_ROWS, NUM_COLS)
    # Assign checkers to players
    players = [PLAYER_CHECKERS[i] for i in range(NUM_PLAYERS)]

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    game_over = False

    while not game_over:
        current_player = players[current_player_idx]
        col_letter = get_player_column_input(current_player, NUM_COLS)
        col_idx = string.ascii_uppercase.index(col_letter)

        if is_column_full(board, col_idx):
            print(f"Column {col_letter} is full. Player {current_player} loses their turn.")
            # Skip to next player (do NOT ask again) according to assignment
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Drop the checker
        row_idx = drop_checker(board, col_idx, current_player)
        clear_screen()
        print_board(board)

        # Check for win
        if check_for_win(board, row_idx, col_idx, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            break

        # Check for draw
        if check_for_draw(board):
            print("It's a draw! The board is full.")
            game_over = True
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
