import os
import random

# Constants you can change
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"
TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 different player tokens
NUM_PLAYERS = 2  # Set between 2 and 5

# ----- Game Functions -----

def clear_screen():
    # Clears the terminal (Linux/macOS). If you're on Windows, use 'cls'.
    os.system('clear')

def make_board(rows, cols):
    return [['.' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    print("  " + " ".join(list(COL_LABELS[:len(board[0])])))
    for r in range(len(board)):
        print(str(r + 1) + " " + " ".join(board[r]))
    print()

def find_open_row(board, col):
    # Returns the bottom-most open row index for the given column, or -1 if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == '.':
            return r
    return -1

def drop_piece(board, row, col, token):
    board[row][col] = token

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (-1, 1)   # diag up-right
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 0
                rr = r
                cc = c
                for k in range(4):
                    if in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                        count += 1
                        rr += dr
                        cc += dc
                    else:
                        break
                if count == 4:
                    return True
    return False

def board_full(move_count, rows, cols):
    return move_count >= rows * cols

def get_valid_column_input(prompt, cols):
    while True:
        choice = input(prompt).strip().upper()
        if len(choice) != 1:
            print("Please enter a single letter (A-{}).".format(COL_LABELS[cols - 1]))
            continue
        if choice not in COL_LABELS[:cols]:
            print("Invalid column. Choose between A and {}.".format(COL_LABELS[cols - 1]))
            continue
        return COL_LABELS.index(choice)

# ----- Main Game -----

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    players = TOKENS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    move_count = 0

    current_index = random.randrange(len(players))

    while True:
        clear_screen()
        print_board(board)
        token = players[current_index]
        print("Players:", " ".join(players))
        print("Current player:", token)

        col = get_valid_column_input("Choose a column (A-{}): ".format(COL_LABELS[COLS - 1]), COLS)

        row = find_open_row(board, col)
        if row == -1:
            print("That column is full. Try another.")
            input("Press Enter to continue...")
            continue

        drop_piece(board, row, col, token)
        move_count += 1

        if check_win(board, token):
            clear_screen()
            print_board(board)
            print("Player", token, "wins! Congratulations!")
            break

        if board_full(move_count, ROWS, COLS):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full.")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)

    print("Game over.")

if __name__ == "__main__":
    main()
