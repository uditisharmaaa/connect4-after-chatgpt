import os
import random
import string

# Constants (you can change ROWS, COLS, and NUM_PLAYERS for testing; submit with 6, 7, and 2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)
    horizontal = "+" + ("---+" * cols))
    for r in range(len(board)):
        print(horizontal)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(horizontal)


def get_valid_column_input(cols):
    valid_letters = set(string.ascii_uppercase[:cols])
    while True:
        user_in = input().strip().upper()
        if len(user_in) == 1 and user_in in valid_letters:
            return ord(user_in) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter:", end=" ")


def place_checker(board, col, symbol):
    # Place from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r][c + 1] == symbol and
                board[r][c + 2] == symbol and board[r][c + 3] == symbol):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == symbol and board[r + 1][c] == symbol and
                board[r + 2][c] == symbol and board[r + 3][c] == symbol):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r + 1][c + 1] == symbol and
                board[r + 2][c + 2] == symbol and board[r + 3][c + 3] == symbol):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r - 1][c + 1] == symbol and
                board[r - 2][c + 2] == symbol and board[r - 3][c + 3] == symbol):
                return True

    return False


def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Ensure constraints
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        return

    player_symbols = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    clear_screen()
    print_board(board)
    while True:
        current_symbol = player_symbols[current_player_index]
        print(f"Player {current_symbol}, please enter a column:", end=" ")

        col = get_valid_column_input(COLS)
        row_placed = place_checker(board, col, current_symbol)

        if row_placed is None:
            # Column full; player loses the turn
            print("Column is full. You lose this turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Successful move: show updated board
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
