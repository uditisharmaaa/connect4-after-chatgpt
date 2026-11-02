import os
import random

# Constants you can change
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 different players
NUM_PLAYERS = 2  # Set from 2 to 5

EMPTY = '.'

def clear():
    # Use the clear command as requested
    os.system('clear')

def make_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Print rows from top to bottom
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(board[r]))
    print()

def get_players():
    n = max(2, min(NUM_PLAYERS, len(PLAYER_SYMBOLS)))
    return PLAYER_SYMBOLS[:n]

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COLUMN_LABELS:
        return COLUMN_LABELS.index(s)
    return None

def find_row_for_col(board, col):
    # Return the lowest empty row index for the given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr = r
    cc = c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def check_win(board, r, c, symbol):
    # Check 4 directions by counting both ways and subtracting 1 (double-count center)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        total = count_in_direction(board, r, c, dr, dc, symbol) + \
                count_in_direction(board, r, c, -dr, -dc, symbol) - 1
        if total >= 4:
            return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == EMPTY:
                return False
    return True

def main():
    players = get_players()
    board = make_board()
    current = random.randrange(len(players))  # random first player

    while True:
        clear()
        print("Connect 4")
        print(f"Players: {' '.join(players)}   (current: {players[current]})")
        print_board(board)

        # Get a valid move
        while True:
            move = input(f"Player {players[current]}, choose column ({COLUMN_LABELS}): ")
            col = col_from_input(move)
            if col is None:
                print("Invalid input. Enter a single letter A-G.")
                continue
            row = find_row_for_col(board, col)
            if row is None:
                print("That column is full. Try another.")
                continue
            break

        # Place the piece
        symbol = players[current]
        board[row][col] = symbol

        # Check for win
        if check_win(board, row, col, symbol):
            clear()
            print_board(board)
            print(f"Player {symbol} wins!")
            break

        # Check for draw
        if is_draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current = (current + 1) % len(players)

if __name__ == "__main__":
    main()
