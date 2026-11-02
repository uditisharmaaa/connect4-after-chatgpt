import os
import random

# Settings (change these if you want)
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
NUM_PLAYERS = 2  # set between 2 and 5

# Make sure NUM_PLAYERS is valid
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    exit(1)

ACTIVE_PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')  # as requested

def make_board():
    board = []
    for _ in range(ROWS):
        board.append(['.'] * COLS)
    return board

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(board[r]))
    print()

def col_from_label(label):
    label = label.strip().upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return -1

def drop_piece(board, col, symbol):
    # Drop from bottom (last row) upwards
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = symbol
            return r, col
    return None  # column full

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

def check_win(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        # count both ways but avoid double counting the starting cell
        total = count_direction(board, r, c, dr, dc, symbol) + count_direction(board, r, c, -dr, -dc, symbol) - 1
        if total >= 4:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == '.':
            return False
    return True

def main():
    board = make_board()
    current_idx = random.randrange(len(ACTIVE_PLAYERS))
    last_move = None

    while True:
        clear_screen()
        print("Connect 4 - {} players: {}".format(NUM_PLAYERS, " ".join(ACTIVE_PLAYERS)))
        print("Columns: " + " ".join(COLUMN_LABELS))
        print_board(board)

        player = ACTIVE_PLAYERS[current_idx]
        move = input("Player {} - choose a column (A-G): ".format(player)).strip().upper()

        if len(move) != 1:
            print("Please enter a single letter A-G. Press Enter to continue.")
            input()
            continue

        col = col_from_label(move)
        if col == -1:
            print("Invalid column. Use A-G. Press Enter to continue.")
            input()
            continue

        if board[0][col] != '.':
            print("That column is full. Press Enter to continue.")
            input()
            continue

        placed = drop_piece(board, col, player)
        if placed is None:
            print("That column is full. Press Enter to continue.")
            input()
            continue

        r, c = placed
        if check_win(board, r, c, player):
            clear_screen()
            print_board(board)
            print("Player {} wins!".format(player))
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % len(ACTIVE_PLAYERS)

if __name__ == "__main__":
    main()
