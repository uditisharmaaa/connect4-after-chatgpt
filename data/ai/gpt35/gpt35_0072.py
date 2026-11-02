import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_CHECKERS_TO_WIN = 4

# Configure game
NUMBER_OF_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUMBER_OF_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Column headers (letters)
    header = "  "
    for c in range(len(board[0])):
        header += f" {chr(ord('A') + c)}  "
    print(header)

    # Board rows and separators
    sep_line = "+" + "---+" * len(board[0])
    for r in range(len(board)):
        print(sep_line)
        row_line = "|"
        for c in range(len(board[0])):
            row_line += f" {board[r][c]} |"
        print(row_line)
    print(sep_line)

def get_valid_column_input(current_player):
    while True:
        inp = input(f"Player {current_player}, please enter a column: ").strip()
        if len(inp) != 1:
            # Must be exactly one character
            continue
        ch = inp.upper()
        if ch < 'A' or ch >= chr(ord('A') + COLUMNS):
            continue
        return ord(ch) - ord('A')

def place_checker(board, column, checker):
    """
    Place the checker in the given column.
    The checker falls to the lowest available row.
    Returns True if placed, False if column is full.
    """
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False  # Column full, lose turn

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - NUM_CHECKERS_TO_WIN + 1):
            if all(board[r][c + i] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - NUM_CHECKERS_TO_WIN + 1):
            if all(board[r + i][c] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True

    # Diagonal (down-right)
    for r in range(rows - NUM_CHECKERS_TO_WIN + 1):
        for c in range(cols - NUM_CHECKERS_TO_WIN + 1):
            if all(board[r + i][c + i] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True

    # Diagonal (up-right)
    for r in range(NUM_CHECKERS_TO_WIN - 1, rows):
        for c in range(cols - NUM_CHECKERS_TO_WIN + 1):
            if all(board[r - i][c + i] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True

    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    if COLUMNS > MAX_COLUMNS:
        print(f"Max supported columns is {MAX_COLUMNS}.")
        return
    if NUMBER_OF_PLAYERS < MIN_PLAYERS or NUMBER_OF_PLAYERS > MAX_PLAYERS:
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return

    board = create_board(ROWS, COLUMNS)

    # Randomly select starting player index
    current_player_index = random.randint(0, NUMBER_OF_PLAYERS -1)

    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_index]
        col = get_valid_column_input(current_checker)

        placed = place_checker(board, col, current_checker)
        print_board(board)

        if not placed:
            # column full => lose turn
            # go to next player
            current_player_index = (current_player_index + 1) % NUMBER_OF_PLAYERS
            continue

        # Check win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUMBER_OF_PLAYERS

if __name__ == "__main__":
    main()
