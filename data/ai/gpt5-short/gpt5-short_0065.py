import os
import random

# Settings (change these for your class/testing)
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Up to 5 players, use the first NUM_PLAYERS from TOKENS
TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set from 2 to 5

EMPTY = '.'

def clear_screen():
    os.system('clear')  # for macOS/Linux; it's okay if it does nothing on some systems

def make_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print header
    print('  ' + ' '.join(COL_LABELS))
    # Print rows from top to bottom
    for r in range(ROWS):
        print(str(ROWS - r) + ' ' + ' '.join(board[r]))
    print()

def drop_piece(board, col, token):
    # Place token in the lowest empty spot in the column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = token
            return r  # return the row where we placed the piece
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_from(board, r, c, token, dr, dc):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == token:
        count += 1
        rr += dr
        cc += dc
    return count

def check_win(board, r, c, token):
    # Check 4 in a row around the last move in 4 direction pairs
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        # Count both directions from the placed piece
        total = 1
        total += check_line(board, r, c, token, dr, dc)
        total += check_line(board, r, c, token, -dr, -dc)
        if total >= 4:
            return True
    return False

def check_line(board, r, c, token, dr, dc):
    cnt = 0
    rr, cc = r + dr, c + dc
    while in_bounds(rr, cc) and board[rr][cc] == token:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def board_full(board):
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True

def get_col_input(current_token):
    while True:
        s = input(f"Player {current_token}, choose a column (A-G): ").strip().upper()
        if len(s) != 1 or s not in COL_LABELS:
            print("Invalid input. Enter a single letter A-G.")
            continue
        col = ord(s) - ord('A')
        return col

def main():
    # Validate NUM_PLAYERS
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    players = TOKENS[:NUM_PLAYERS]

    board = make_board()
    current = random.randrange(len(players))  # random first player

    while True:
        clear_screen()
        print_board(board)
        token = players[current]

        # Get a valid playable column
        while True:
            col = get_col_input(token)
            if board[0][col] != EMPTY:
                print("That column is full. Try another one.")
                continue
            break

        row = drop_piece(board, col, token)

        # Check win
        if check_win(board, row, col, token):
            clear_screen()
            print_board(board)
            print(f"Player {token} wins!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current = (current + 1) % len(players)

if __name__ == "__main__":
    main()
