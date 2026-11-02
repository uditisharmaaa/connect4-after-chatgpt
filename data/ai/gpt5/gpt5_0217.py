import os
import random
import string
import sys

# Constants (change these for different configurations)
BOARD_ROWS = 6
BOARD_COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Validate constants
BOARD_COLS = max(1, min(26, BOARD_COLS))
NUM_PLAYERS = max(2, min(5, NUM_PLAYERS))
PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])
    # Header with column letters
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print(sep)


def get_column_index_from_input(user_input, cols):
    if len(user_input) != 1:
        return None
    ch = user_input.upper()
    letters = string.ascii_uppercase[:cols]
    if ch in letters:
        return letters.index(ch)
    return None


def get_valid_column_input(player_token, cols):
    while True:
        user_input = input(f"Player {player_token}, please enter a column: ").strip()
        col = get_column_index_from_input(user_input, cols)
        if col is None:
            print("Invalid input. Please enter a valid column letter.")
            continue
        return col


def drop_checker(board, col, token):
    rows = len(board)
    # place from bottom up
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None  # column full


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    L = WIN_LENGTH

    # Horizontal
    for r in range(rows):
        for c in range(cols - L + 1):
            if all(board[r][c + k] == token for k in range(L)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - L + 1):
            if all(board[r + k][c] == token for k in range(L)):
                return True

    # Diagonal down-right
    for r in range(rows - L + 1):
        for c in range(cols - L + 1):
            if all(board[r + k][c + k] == token for k in range(L)):
                return True

    # Diagonal down-left
    for r in range(rows - L + 1):
        for c in range(L - 1, cols):
            if all(board[r + k][c - k] == token for k in range(L)):
                return True

    return False


def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True


def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        token = PLAYER_TOKENS[current_player_index]

        # Ask for input
        col = get_valid_column_input(token, BOARD_COLS)

        # Try to drop checker
        result = drop_checker(board, col, token)
        if result is None:
            # Column full -> turn is lost
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {token} loses the turn.")
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Successful move; print board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, token):
            print(f"Player {token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
