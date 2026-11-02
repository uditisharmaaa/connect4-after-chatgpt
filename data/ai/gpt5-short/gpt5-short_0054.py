# Connect 4 (6x7) for 2–5 players using basic Python
# Columns labeled A-G, random first player, input validation, win/draw checks
# Clears screen each turn with os.system('clear')

import os
import random

# --------- Configurable constants ---------
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5
# ------------------------------------------

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---+---+---+---+---+---+---+")

def col_letter_to_index(letter):
    return ord(letter) - ord('A')

def is_valid_col_letter(s):
    if len(s) != 1:
        return False
    ch = s.upper()
    return 'A' <= ch <= 'G'

def column_full(board, col):
    return board[0][col] != ' '

def drop_piece(board, col, symbol):
    # Place symbol in the lowest empty row of the given column.
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1  # Column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr = r
    cc = c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        if count == 4:
            return True
        rr += dr
        cc += dc
    return False

def check_win(board, symbol):
    # Check horizontal, vertical, and both diagonals
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != symbol:
                continue
            # Right
            if check_direction(board, r, c, 0, 1, symbol):
                return True
            # Down
            if check_direction(board, r, c, 1, 0, symbol):
                return True
            # Down-right
            if check_direction(board, r, c, 1, 1, symbol):
                return True
            # Down-left
            if check_direction(board, r, c, 1, -1, symbol):
                return True
    return False

def check_draw(board):
    # If top row has any spaces, it's not a draw
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_move_input(current_symbol, board):
    while True:
        move = input("Player " + current_symbol + ", choose a column (A-G): ").strip().upper()
        if not is_valid_col_letter(move):
            print("Invalid input. Please enter a single letter A-G.")
            continue
        col = col_letter_to_index(move)
        if column_full(board, col):
            print("That column is full. Choose another.")
            continue
        return col

def main():
    # Validate number of players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()

    current_index = random.randint(0, NUM_PLAYERS - 1)
    winner = None

    while True:
        clear_screen()
        print_board(board)
        print("Players: " + " ".join(symbols))
        print("Current: " + symbols[current_index])

        col = get_move_input(symbols[current_index], board)
        row = drop_piece(board, col, symbols[current_index])

        # Safety check; should not happen because we validate before
        if row == -1:
            print("Unexpected error: column full after validation.")
            continue

        if check_win(board, symbols[current_index]):
            winner = symbols[current_index]
            clear_screen()
            print_board(board)
            print("Player " + winner + " wins!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
