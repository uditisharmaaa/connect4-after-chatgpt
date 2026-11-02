import os
import random
import string

# Constants (you can change ROWS, COLS, NUM_PLAYERS for testing; max 26 columns)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constants
if COLS > 26:
    COLS = 26
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

PLAYERS = CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    cols = len(board[0])
    # Header letters
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Board grid
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)

def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def get_lowest_empty_row(board, col):
    # Start from bottom row
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, col, symbol):
    r = get_lowest_empty_row(board, col)
    if r is None:
        return False
    board[r][col] = symbol
    return True

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, down-right, down-left
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr = r + dr
                cc = c + dc
                while count < WIN_LENGTH and in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LENGTH:
                    return True
    return False

def get_valid_column_input(cols, current_symbol):
    while True:
        user_input = input(f"Player {current_symbol}, please enter a column: ")
        user_input = user_input.strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        col = ord(user_input) - ord('A')
        if col < 0 or col >= cols:
            print("Invalid input. Column is out of range.")
            continue
        return col

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        current_symbol = PLAYERS[current_player_index]
        col = get_valid_column_input(COLS, current_symbol)

        placed = drop_checker(board, col, current_symbol)
        if not placed:
            print("Column is full. Turn lost.")
            # Even if no change, reprint the board as per instructions
            clear_screen()
            print_board(board)
            # Advance to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        clear_screen()
        print_board(board)

        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        if is_board_full(board):
            print("Draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
