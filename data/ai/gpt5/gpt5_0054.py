import os
import random
import string

# Constants (adjustable; submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5

# Player symbols in order
SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header with column letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print(sep)

def get_column_input(valid_max_col):
    while True:
        user_input = input().strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter (e.g., A).")
            continue
        ch = user_input.upper()
        if ch < 'A' or ch > chr(ord('A') + valid_max_col - 1):
            print("Invalid column. Please enter a letter between A and {}.".format(chr(ord('A') + valid_max_col - 1)))
            continue
        return ord(ch) - ord('A')

def place_checker(board, col, symbol):
    # Place in lowest available row (from bottom up)
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r, col
    return None  # column full

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    needed = 4

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            # Check right
            if c + needed - 1 < cols:
                if all(board[r][c + k] == symbol for k in range(needed)):
                    return True
            # Check down
            if r + needed - 1 < rows:
                if all(board[r + k][c] == symbol for k in range(needed)):
                    return True
            # Check diag down-right
            if r + needed - 1 < rows and c + needed - 1 < cols:
                if all(board[r + k][c + k] == symbol for k in range(needed)):
                    return True
            # Check diag down-left
            if r + needed - 1 < rows and c - (needed - 1) >= 0:
                if all(board[r + k][c - k] == symbol for k in range(needed)):
                    return True
    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Safety checks
    if COLS > 26:
        print("Maximum supported columns is 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        symbol = SYMBOLS[current_player_index]
        print("Player {}, please enter a column:".format(symbol))

        col = get_column_input(COLS)

        # Try to place checker
        placed = place_checker(board, col, symbol)

        clear_screen()
        print_board(board)

        if placed is None:
            # Column full: lose turn
            print("Column is full. Player {} loses the turn.".format(symbol))
        else:
            # Check for win
            if check_win(board, symbol):
                print("Player {} won!".format(symbol))
                break
            # Check for draw
            if is_draw(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
