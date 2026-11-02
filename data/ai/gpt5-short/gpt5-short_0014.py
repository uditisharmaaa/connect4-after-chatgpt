import os
import random

# Constants (you can change NUM_PLAYERS between 2 and 5)
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set this to 2, 3, 4, or 5

def clear_screen():
    os.system('clear')

def make_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---" * COLS + "+")

def letter_to_col(letter):
    if letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(letter)
    return -1

def is_column_full(board, col):
    return board[0][col] != ' '

def drop_piece(board, col, symbol):
    # Drop from bottom up; return the row index where it lands
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r
    return -1  # should not happen if checked before

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

def is_winning_move(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        # Count in positive direction (excluding the starting cell)
        pos = count_direction(board, r + dr, c + dc, dr, dc, symbol)
        # Count in negative direction (excluding the starting cell)
        neg = count_direction(board, r - dr, c - dc, -dr, -dc, symbol)
        if 1 + pos + neg >= 4:
            return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_valid_move(board, current_symbol):
    while True:
        move = input(f"Player {current_symbol}, choose a column (A-G): ").strip().upper()
        if len(move) != 1:
            print("Please enter a single letter from A to G.")
            continue
        col = letter_to_col(move)
        if col == -1:
            print("Invalid column. Please choose from A to G.")
            continue
        if is_column_full(board, col):
            print("That column is full. Choose another.")
            continue
        return col

def main():
    # Validate player count
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = make_board()

    current_index = random.randrange(len(players))
    winner = None

    while True:
        clear_screen()
        print_board(board)
        current_symbol = players[current_index]

        col = get_valid_move(board, current_symbol)
        row = drop_piece(board, col, current_symbol)

        clear_screen()
        print_board(board)

        if is_winning_move(board, row, col, current_symbol):
            winner = current_symbol
            print(f"Player {winner} wins!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % len(players)

if __name__ == "__main__":
    main()
