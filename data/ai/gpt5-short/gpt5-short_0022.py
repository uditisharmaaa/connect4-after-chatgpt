import os
import random

# Constants you can adjust
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5

EMPTY = '.'

def clear_screen():
    os.system('clear')  # As requested

def make_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(EMPTY)
        board.append(row)
    return board

def print_board(board, current_player_symbol=None):
    clear_screen()
    print("Connect 4 - {} rows x {} cols (A-G)".format(ROWS, COLS))
    if current_player_symbol is not None:
        print("Current player: {}".format(current_player_symbol))
    # Column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Board rows
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(board[r]))
    print()

def get_active_players():
    n = NUM_PLAYERS
    if n < 2:
        n = 2
    if n > 5:
        n = 5
    return PLAYER_SYMBOLS[:n]

def col_from_input(user_input):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return -1
    if user_input in COLUMN_LABELS:
        return COLUMN_LABELS.index(user_input)
    return -1

def find_drop_row(board, col):
    # Return row index where a disc would land in this column, or -1 if full
    for r in range(ROWS - 1, -1, -1):  # start from bottom
        if board[r][col] == EMPTY:
            return r
    return -1

def drop_disc(board, col, symbol):
    r = find_drop_row(board, col)
    if r == -1:
        return -1
    board[r][col] = symbol
    return r

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == EMPTY:
                return False
    return True

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

def check_win_from_cell(board, r, c):
    symbol = board[r][c]
    if symbol == EMPTY:
        return False

    # Directions: horizontal (0,1), vertical (1,0), diag down-right (1,1), diag up-right (-1,1)
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        # Count both directions from the placed disc
        forward = count_direction(board, r, c, dr, dc, symbol)
        backward = count_direction(board, r, c, -dr, -dc, symbol)
        # We counted the cell twice, so subtract 1
        total = forward + backward - 1
        if total >= 4:
            return True
    return False

def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    active_players = get_active_players()
    total_players = len(active_players)
    board = make_board()

    # Random first player
    current_index = random.randrange(total_players)

    while True:
        current_symbol = active_players[current_index]
        print_board(board, current_symbol)

        # Prompt
        user_input = input("Player {} - choose column (A-G): ".format(current_symbol))
        col = col_from_input(user_input)
        if col == -1:
            print("Invalid input. Please enter a letter A-G. Press Enter to continue.")
            input()
            continue

        row = drop_disc(board, col, current_symbol)
        if row == -1:
            print("Column {} is full. Press Enter to continue.".format(COLUMN_LABELS[col]))
            input()
            continue

        # Check win
        if check_win_from_cell(board, row, col):
            print_board(board, current_symbol)
            print("Player {} wins!".format(current_symbol))
            break

        # Check draw
        if board_full(board):
            print_board(board, None)
            print("It's a draw!")
            break

        # Next player
        current_index = next_player_index(current_index, total_players)

    print("Game over.")

if __name__ == "__main__":
    main()
