import os
import random

# Constants you can change
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # set between 2 and 5

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Clear the screen each time we print
    os.system('clear')
    print("  " + " ".join(list(COLUMN_LABELS)))
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c])
        print("| " + " ".join(row_str))
    print()

def get_col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COLUMN_LABELS:
        return COLUMN_LABELS.index(s)
    return None

def drop_piece(board, col, symbol):
    # Returns the row where the piece landed, or None if column full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        count = 1
        # forward
        rr = r + dr
        cc = c + dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        # backward
        rr = r - dr
        cc = c - dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    moves_made = 0
    start_index = random.randrange(NUM_PLAYERS)
    current_turn = 0

    while True:
        current_player_index = (start_index + current_turn) % NUM_PLAYERS
        symbol = players[current_player_index]

        print_board(board)
        print(f"Players: {', '.join(players)}")
        print(f"Turn: {symbol}")
        user_input = input("Choose a column (A-G): ")

        col = get_col_from_input(user_input)
        if col is None:
            print("Invalid input. Please enter a letter A-G. Press Enter to continue.")
            input()
            continue

        row = drop_piece(board, col, symbol)
        if row is None:
            print("That column is full. Press Enter to continue.")
            input()
            continue

        moves_made += 1

        if check_win(board, row, col, symbol):
            print_board(board)
            print(f"Player {symbol} wins!")
            break

        if moves_made == ROWS * COLS:
            print_board(board)
            print("It's a draw!")
            break

        current_turn += 1

if __name__ == "__main__":
    main()
