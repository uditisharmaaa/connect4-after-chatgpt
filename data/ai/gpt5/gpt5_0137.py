import os
import random
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    clear_screen()

    # Header with column letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)


def get_valid_column_input(cols):
    valid_letters = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        s = input().strip().upper()
        if len(s) != 1:
            print("Invalid input. Please enter a single column letter:")
            continue
        if s not in valid_letters:
            print("Invalid column. Please enter a letter between {} and {}:".format(valid_letters[0], valid_letters[-1]))
            continue
        return valid_letters.index(s)


def place_checker(board, col, symbol):
    # Place from bottom up
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col
    return None  # Column full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    target = 4

    # Horizontal check
    for r in range(rows):
        for c in range(cols - target + 1):
            if all(board[r][c + k] == symbol for k in range(target)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - target + 1):
            if all(board[r + k][c] == symbol for k in range(target)):
                return True

    # Diagonal down-right
    for r in range(rows - target + 1):
        for c in range(cols - target + 1):
            if all(board[r + k][c + k] == symbol for k in range(target)):
                return True

    # Diagonal up-right
    for r in range(target - 1, rows):
        for c in range(cols - target + 1):
            if all(board[r - k][c + k] == symbol for k in range(target)):
                return True

    return False


def check_draw(board):
    # Draw if no spaces left in top row (or anywhere)
    for r in board:
        if " " in r:
            return False
    return True


def main():
    # Validate constants
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    print_board(board)

    while True:
        current_symbol = symbols[current_player]
        print("Player {}, please enter a column:".format(current_symbol))

        col = get_valid_column_input(COLS)

        # Try to place checker
        result = place_checker(board, col, current_symbol)
        if result is None:
            # Column full, player loses turn
            print("Column is full. Turn lost.")
            input("Press Enter to continue...")
            print_board(board)
            # Next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Successful move; check for win/draw
        print_board(board)

        if check_win(board, current_symbol):
            print("Player {} won!".format(current_symbol))
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
