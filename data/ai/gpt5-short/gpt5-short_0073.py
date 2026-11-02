import os
import random

# Constants: set number of players between 2 and 5
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # up to 5 symbols

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COL_LABELS))
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c])
        print(str(r+1) + ' ' + ' '.join(row_str))
    print()

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COL_LABELS:
        return COL_LABELS.index(s)
    return None

def is_column_full(board, c):
    return board[0][c] != ' '

def drop_piece(board, c, symbol):
    # place from bottom up
    for r in range(ROWS - 1, -1, -1):
        if board[r][c] == ' ':
            board[r][c] = symbol
            return r, c
    return None  # column full (shouldn't happen if checked)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr = r
    cc = c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def is_winner(board, r, c, symbol):
    # check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        # count in both directions, subtract 1 to avoid double counting starting cell
        total = count_direction(board, r, c, dr, dc, symbol) + count_direction(board, r, c, -dr, -dc, symbol) - 1
        if total >= 4:
            return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()
    current = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print("Connect 4 - {} players: {}".format(NUM_PLAYERS, ' '.join(symbols)))
        print("Player order: " + ' -> '.join(symbols))
        print("Current player: {}".format(symbols[current]))
        print_board(board)

        move = input("Choose a column (A-G): ")
        col = col_from_input(move)
        if col is None:
            print("Invalid input. Please enter a letter A-G. Press Enter to continue.")
            input()
            continue
        if is_column_full(board, col):
            print("That column is full. Press Enter to continue.")
            input()
            continue

        r, c = drop_piece(board, col, symbols[current])

        if is_winner(board, r, c, symbols[current]):
            clear_screen()
            print_board(board)
            print("Player {} wins!".format(symbols[current]))
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
