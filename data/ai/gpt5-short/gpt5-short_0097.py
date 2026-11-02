# Connect 4 (6x7) for 2-5 players
# Players and settings
NUM_PLAYERS = 2  # change to 2-5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # first NUM_PLAYERS are used

import os
import random

ROWS = 6
COLS = 7
EMPTY = ' '
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def clear_screen():
    os.system('clear')  # use 'cls' on Windows if needed

def make_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board, current_player_symbol=None):
    clear_screen()
    print("Connect 4 - 6 rows x 7 columns")
    print("Players:", ' '.join(PLAYER_SYMBOLS[:NUM_PLAYERS]))
    if current_player_symbol:
        print("Turn:", current_player_symbol)
    print('  ' + ' '.join(COL_LABELS))
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c] if board[r][c] != EMPTY else '.')
        print(str(ROWS - r) + ' ' + ' '.join(row_str))
    print()

def col_from_input(s):
    if not s:
        return None
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COL_LABELS:
        return COL_LABELS.index(s)
    return None

def drop_piece(board, col, symbol):
    # place piece in lowest empty slot in column; return row index or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = symbol
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_dir(board, r, c, dr, dc, symbol):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def is_win(board, r, c, symbol):
    # check all 4 directions by counting both ways and subtracting 1 overlap
    dirs = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in dirs:
        total = count_dir(board, r, c, dr, dc, symbol) + count_dir(board, r, c, -dr, -dc, symbol) - 1
        if total >= 4:
            return True
    return False

def is_draw(board):
    # draw if top row has no empty cells
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True

def main():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = make_board()
    current_index = random.randint(0, NUM_PLAYERS - 1)
    winner = None

    while True:
        current_symbol = players[current_index]
        print_board(board, current_symbol)
        # get valid input
        while True:
            move = input("Choose a column (A-G): ")
            col = col_from_input(move)
            if col is None:
                print("Invalid input. Enter a single letter A-G.")
                continue
            row = drop_piece(board, col, current_symbol)
            if row is None:
                print("That column is full. Try another.")
                continue
            break

        # check for win or draw
        if is_win(board, row, col, current_symbol):
            winner = current_symbol
            print_board(board, current_symbol)
            print("Player", winner, "wins!")
            break
        if is_draw(board):
            print_board(board, current_symbol)
            print("It's a draw!")
            break

        # next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
