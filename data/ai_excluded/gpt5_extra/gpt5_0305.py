import os
import random
import string

# Constants (change these if you want to try different settings)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
WIN_LENGTH = 4  # always 4 per assignment

SYMBOLS = ["X", "O", "V", "H", "M"]  # up to 5 players

# Basic checks
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5")
if COLS > 26 or COLS < 1:
    raise ValueError("COLS must be between 1 and 26")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1")

PLAYER_SYMBOLS = SYMBOLS[:NUM_PLAYERS]


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    os.system('clear')
    rows = len(board)
    cols = len(board[0])

    # Header with letters
    letters = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(letters))

    # Board grid
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def is_valid_column_letter(col_letter, cols):
    if len(col_letter) != 1:
        return False
    if col_letter not in string.ascii_uppercase[:cols]:
        return False
    return True


def get_column_index_from_letter(col_letter):
    return ord(col_letter) - ord('A')


def column_is_full(board, col):
    return board[0][col] != " "


def drop_checker(board, col, symbol):
    # Place in the lowest available row in this column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True
    return False  # column full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, diag down-right, diag down-left
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr = r + dr
                cc = c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == WIN_LENGTH:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        if " " in row:
            return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial empty board
    print_board(board)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_index]
        # Prompt and validate input (invalid input retries)
        while True:
            user_in = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
            if is_valid_column_letter(user_in, COLS):
                col_index = get_column_index_from_letter(user_in)
                break
            else:
                print("Invalid input. Please enter a valid uppercase column letter shown above.")

        # Try to place checker
        if column_is_full(board, col_index):
            # Turn is lost if column is full
            print("That column is full. You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Show board after turn
            print_board(board)
            continue
        else:
            drop_checker(board, col_index, current_symbol)

        # After placing, check for win
        if check_win(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        print_board(board)


if __name__ == "__main__":
    main()
