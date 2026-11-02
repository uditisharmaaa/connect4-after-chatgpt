import os
import random
import string
import sys

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2  # Allowed from 2 to 5

CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_SYMBOLS = CHECKERS[:PLAYERS]
EMPTY_CELL = " "

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    rows = len(board)
    alphabet = string.ascii_uppercase

    # Print column headers
    print("  ", end="")
    for c in range(cols):
        print(" " + alphabet[c] + " ", end="")
    print()
    # Print separator
    print("+" + "---+" * cols)
    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(" %s |" % cell, end="")
        print()
        print("+" + "---+" * cols)

def get_valid_columns(board):
    cols = len(board[0])
    valid = []
    for c in range(cols):
        if board[0][c] == EMPTY_CELL:
            valid.append(c)
    return valid

def get_column_index(input_col, cols):
    if len(input_col) != 1:
        return None
    input_col = input_col.upper()
    idx = ord(input_col) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None

def make_move(board, col, symbol):
    """
    Try to place symbol in the column col. Returns (row_index, col) if successful, else None.
    """
    for row in reversed(range(len(board))):  # Start from bottom
        if board[row][col] == EMPTY_CELL:
            board[row][col] = symbol
            return (row, col)
    return None

def is_full(board):
    for row in board:
        if EMPTY_CELL in row:
            return False
    return True

def check_winner(board, last_move, symbol, connect=4):
    """
    Check all directions from the last move to see if there are four in a row.
    last_move: (row, col)
    symbol: current player's symbol
    """
    rows = len(board)
    cols = len(board[0])
    row, col = last_move

    dir_vectors = [
        (0, 1),   # horizonal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in dir_vectors:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= connect:
            return True
    return False

def main():
    # Seed the random module for reproducibility (can remove for more randomness)
    random.seed()
    # Initialize board
    board = create_board(ROWS, COLS)
    cols = COLS
    rows = ROWS
    alphabet = string.ascii_uppercase

    # Pick a random starting player
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        print("Player %s, please enter a column:" % PLAYER_SYMBOLS[current_player])
        input_col = input("> ").strip()

        # Input validation
        col_idx = get_column_index(input_col, cols)
        if col_idx is None or col_idx < 0 or col_idx >= cols:
            print("Invalid input. Please enter a valid column letter (A-%s)." % alphabet[cols-1])
            input("Press Enter to continue...")
            continue

        # Check if the column is full
        if board[0][col_idx] != EMPTY_CELL:
            print("Column %s is already full. You lose your turn." % alphabet[col_idx])
            input("Press Enter to continue...")  # Wait for user
            # Lose turn, go to next player
            current_player = (current_player + 1) % PLAYERS
            continue

        # Place checker
        move = make_move(board, col_idx, PLAYER_SYMBOLS[current_player])
        if move is None:
            print("Unexpected error: could not place checker.")
            input("Press Enter to continue...")
            continue

        # Check for winner
        if check_winner(board, move, PLAYER_SYMBOLS[current_player], connect=4):
            clear_screen()
            print_board(board)
            print("Player %s won!" % PLAYER_SYMBOLS[current_player])
            break

        # Check for draw
        if is_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
