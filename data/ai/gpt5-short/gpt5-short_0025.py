import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"

# Change this to choose how many players (2 to 5)
NUM_PLAYERS = 2

# Symbols used by up to 5 players, in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']


def clear_screen():
    # As requested
    os.system('clear')


def make_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board, current_player_symbol=None):
    clear_screen()
    print(" Connect 4")
    print(" Columns: " + " ".join(COL_LABELS))
    print("-" * (2 * COLS + 9))

    # Print from top row to bottom row
    for r in range(ROWS):
        row_str = "| "
        for c in range(COLS):
            row_str += board[r][c] + " "
        row_str += "|"
        print(row_str)

    print("-" * (2 * COLS + 9))
    if current_player_symbol:
        print(f"Player {current_player_symbol}'s turn. Choose a column (A-G) or Q to quit.")


def col_full(board, col):
    return board[0][col] != ' '


def drop_piece(board, col, symbol):
    # Place in the lowest empty spot in the column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None  # Shouldn't happen if checked before


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_winner(board, symbol):
    # Check all directions for 4 in a row

    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and board[r][c+1] == symbol and
                board[r][c+2] == symbol and board[r][c+3] == symbol):
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (board[r][c] == symbol and board[r+1][c] == symbol and
                board[r+2][c] == symbol and board[r+3][c] == symbol):
                return True

    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and board[r+1][c+1] == symbol and
                board[r+2][c+2] == symbol and board[r+3][c+3] == symbol):
                return True

    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and board[r-1][c+1] == symbol and
                board[r-2][c+2] == symbol and board[r-3][c+3] == symbol):
                return True

    return False


def check_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True


def get_valid_column_input(prompt):
    while True:
        choice = input(prompt).strip().upper()
        if choice == 'Q':
            return 'Q'
        if len(choice) == 1 and choice in COL_LABELS:
            return choice
        print("Invalid input. Enter a column letter A-G, or Q to quit.")


def main():
    # Setup number of players safely
    n = NUM_PLAYERS
    if n < 2:
        n = 2
    if n > 5:
        n = 5

    players = PLAYER_SYMBOLS[:n]
    board = make_board()

    # Pick random first player
    current_index = random.randint(0, n - 1)

    while True:
        current_symbol = players[current_index]
        print_board(board, current_symbol)

        # Ask for input
        col_input = get_valid_column_input("Your move: ")
        if col_input == 'Q':
            print("Game quit. Goodbye!")
            return

        col = COL_LABELS.index(col_input)

        # Validate column not full
        if col_full(board, col):
            print("That column is full. Press Enter to try again...")
            input()
            continue

        # Drop the piece
        drop_piece(board, col, current_symbol)

        # Check for win
        if check_winner(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins! Press Enter to exit.")
            input()
            return

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! Press Enter to exit.")
            input()
            return

        # Next player
        current_index = (current_index + 1) % n


if __name__ == "__main__":
    main()
