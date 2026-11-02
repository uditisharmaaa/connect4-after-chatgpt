import os
import random
import string
import sys

# Configuration constants (submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # supports 2 to 5
WIN_N = 4

SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(n):
    if n < 1 or n > 26:
        raise ValueError("Number of columns must be between 1 and 26.")
    return list(string.ascii_uppercase[:n])

def print_board(board, labels):
    cols = len(board[0])
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row_cells = [f" {board[r][c]} " for c in range(cols)]
        print("|" + "|".join(row_cells) + "|")
        print(sep)

def get_column_input(current_symbol, valid_labels):
    while True:
        try:
            user_in = input(f"Player {current_symbol}, please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)
        if len(user_in) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        ch = user_in.upper()
        if ch not in valid_labels:
            print("Invalid column. Please enter one of: " + ", ".join(valid_labels))
            continue
        return valid_labels.index(ch)

def place_checker(board, col, symbol):
    # Place at lowest available row in the given column. Return True if placed, False if column full.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return True
    return False

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    n = WIN_N

    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                rr, cc = r, c
                count = 0
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == n:
                        return True
                    rr += dr
                    cc += dc
    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    players = SYMBOLS[:NUM_PLAYERS]
    labels = column_labels(COLS)
    board = create_board(ROWS, COLS)

    current_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board, labels)

    while True:
        current_symbol = players[current_idx]
        col = get_column_input(current_symbol, labels)

        placed = place_checker(board, col, current_symbol)
        if not placed:
            # Turn is invalid and player loses the turn
            clear_screen()
            print_board(board, labels)
            print(f"Column {labels[col]} is full. Player {current_symbol} loses the turn.")
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move, update display and check game state
        clear_screen()
        print_board(board, labels)

        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
