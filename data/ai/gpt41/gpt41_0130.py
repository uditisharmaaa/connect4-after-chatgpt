import os
import random
import string

# --------- CONSTANTS ---------
BOARD_ROWS = 6         # Number of rows
BOARD_COLS = 7         # Number of columns (max 26)
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # At most 5 symbols
NUM_PLAYERS = 2        # Set to 2 for assignment submission

WIN_LENGTH = 4         # Number of checkers in a row needed to win

# --------- FUNCTIONS ---------

def clear_screen():
    """Clears the game screen using the OS's clear command."""
    os.system('clear')

def create_board(rows, cols):
    """Creates the game board as a 2D list initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """
    Prints the current state of the board.
    The columns are labeled from 'A' onwards.
    """
    col_headers = "  " + "   ".join([string.ascii_uppercase[i] for i in range(cols)])
    separator = "+" + "---+" * cols
    print(col_headers)
    print(separator)
    for row in board:
        row_str = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_str)
        print(separator)

def get_valid_columns(board):
    """Returns a list of column indices that are not full."""
    valid_cols = []
    for col in range(len(board[0])):
        if any(board[row][col] == " " for row in range(len(board))):
            valid_cols.append(col)
    return valid_cols

def get_player_input(player_symbol, board):
    """Prompts the current player to select a column and validates the input."""
    valid_cols = get_valid_columns(board)
    col_letters = [string.ascii_uppercase[col] for col in valid_cols]
    while True:
        inp = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in string.ascii_uppercase[:len(board[0])]:
            print("Invalid input; please enter a valid column letter.")
            continue
        col = string.ascii_uppercase.index(inp)
        if col not in valid_cols:
            print("Column is full or invalid; please choose another column.")
            continue
        return col

def drop_checker(board, col, player_symbol):
    """
    Inserts the player's checker into the specified column.
    Returns True if placed, False if the column is full (shouldn't happen with validation).
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return row, col  # Return the placement coordinates
    return None, None

def check_win(board, last_row, last_col, player_symbol):
    """
    Checks if the player has achieved 4 in a row (horizontal, vertical, or diagonal)
    by checking from the last placed checker.
    """
    def count(dx, dy):
        count = 0
        x, y = last_row, last_col
        while 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == player_symbol:
            count += 1
            x += dx
            y += dy
        return count - 1  # exclude starting cell (will sum both directions)

    # 4 directions: (dx, dy): horizontal, vertical, 2 diagonals
    directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]
    for dx, dy in directions:
        total = 1 + count(dx, dy) + count(-dx, -dy)
        if total >= WIN_LENGTH:
            return True
    return False

def is_board_full(board):
    """Returns True if the board is full (no spaces left), else False."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Set up game variables
    rows = BOARD_ROWS
    cols = BOARD_COLS
    num_players = NUM_PLAYERS
    player_symbols = PLAYER_SYMBOLS[:num_players]

    # Create board
    board = create_board(rows, cols)

    # Randomly choose first player
    current_player_idx = random.randint(0, num_players - 1)

    # Game loop
    clear_screen()
    print_board(board, cols)

    while True:
        player_symbol = player_symbols[current_player_idx]
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("The board is full! It's a draw.")
            break

        col = get_player_input(player_symbol, board)
        row, col = drop_checker(board, col, player_symbol)

        clear_screen()
        print_board(board, cols)

        # Check for win condition
        if check_win(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The board is full! It's a draw.")
            break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
