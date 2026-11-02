# Simple Connect 4 (6x7) for 2–5 players
# Players are chosen from X, O, V, H, M. Set NUM_PLAYERS to 2–5.

import os
import random

ROWS = 6
COLS = 7

# Configure players here
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # change to 3, 4, or 5 if you want more players

# Clear the screen (works on macOS/Linux; on Windows use 'cls')
def clear_screen():
    os.system('clear')

def make_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Column labels A-G
    print("  " + " ".join([chr(ord('A') + i) for i in range(COLS)]))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(board[r]))
    print()

def col_from_input(s):
    if len(s) != 1:
        return -1
    ch = s.upper()
    if ch < 'A' or ch > 'G':
        return -1
    return ord(ch) - ord('A')

def drop_piece(board, col, symbol):
    # Drop piece in the lowest empty spot in the column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r
    return -1  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_dir(board, r, c, dr, dc, symbol):
    count = 0
    rr = r
    cc = c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def check_win(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag /, diag \
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # Count both directions from the last placed piece
        total = count_dir(board, r, c, dr, dc, symbol) + count_dir(board, r, c, -dr, -dc, symbol) - 1
        if total >= 4:
            return True
    return False

def board_full(board):
    # If top row has any space, board not full
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    symbols = PLAYERS[:NUM_PLAYERS]
    board = make_board()
    current = random.randrange(NUM_PLAYERS)  # random first player

    while True:
        clear_screen()
        print_board(board)
        player_symbol = symbols[current]
        choice = input("Player " + player_symbol + " - choose column (A-G): ").strip()
        col = col_from_input(choice)
        if col == -1:
            print("Invalid input. Enter a single letter A-G. Press Enter to continue.")
            input()
            continue

        row = drop_piece(board, col, player_symbol)
        if row == -1:
            print("That column is full. Press Enter to continue.")
            input()
            continue

        # Check for win
        if check_win(board, row, col, player_symbol):
            clear_screen()
            print_board(board)
            print("Player " + player_symbol + " wins!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
