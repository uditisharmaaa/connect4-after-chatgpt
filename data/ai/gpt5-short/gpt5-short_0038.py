import os
import random

# Constants you can change
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"
ALL_PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set between 2 and 5

EMPTY = '.'

def clear_screen():
    os.system('clear')  # use 'cls' on Windows if needed

def make_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(EMPTY)
        board.append(row)
    return board

def print_board(board, players, current_symbol=None):
    clear_screen()
    print("Connect 4")
    print("Players:", ' '.join(players))
    if current_symbol is not None:
        print("Turn:", current_symbol)
    print("  " + ' '.join(list(COL_LABELS)))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + ' '.join(board[r]))
    print()

def get_column_input(players, current_symbol):
    while True:
        choice = input(f"Player {current_symbol}, choose a column (A-{COL_LABELS[-1]}): ").strip().upper()
        if len(choice) != 1 or choice not in COL_LABELS:
            print("Invalid input. Enter a single letter between A and " + COL_LABELS[-1] + ".")
            continue
        return COL_LABELS.index(choice)

def drop_piece(board, col, symbol):
    # Place in the lowest available row in this column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = symbol
            return r
    return -1  # column full

def on_board(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    count = 0
    r = start_r
    c = start_c
    while on_board(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, last_r, last_c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        # Count in both directions from the last placed piece
        total = 0
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        total -= 1  # counted the center twice
        if total >= 4:
            return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True

def main():
    # Validate NUM_PLAYERS
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    players = ALL_PLAYERS[:NUM_PLAYERS]
    board = make_board()

    current_index = random.randrange(len(players))
    current_symbol = players[current_index]

    while True:
        print_board(board, players, current_symbol)
        col = get_column_input(players, current_symbol)

        row = drop_piece(board, col, current_symbol)
        if row == -1:
            print("That column is full. Try another.")
            input("Press Enter to continue...")
            continue

        # Check for win
        if is_winning_move(board, row, col, current_symbol):
            print_board(board, players)
            print(f"Player {current_symbol} wins!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board, players)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)
        current_symbol = players[current_index]

if __name__ == "__main__":
    main()
