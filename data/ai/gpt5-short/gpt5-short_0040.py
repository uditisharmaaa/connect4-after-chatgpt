import os
import random
import sys

# Constants (adjust as needed for your class)
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"
PLAYER_TOKENS = ("X", "O", "V", "H", "M")
NUM_PLAYERS = 2  # set to 2..5

EMPTY = "."

def clear_screen():
    # As requested
    os.system('clear')

def make_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board, players, current_idx):
    clear_screen()
    print("Connect 4 — {} players: {}".format(len(players), " ".join(players)))
    print("Current: {}".format(players[current_idx]))
    print("  " + " ".join(list(COL_LABELS)))
    for r in range(ROWS):
        print("| " + " ".join(board[r]) + " |")
    print("  " + " ".join(list(COL_LABELS)))

def col_to_index(col_char):
    col_char = col_char.upper()
    if col_char in COL_LABELS:
        return COL_LABELS.index(col_char)
    return None

def is_valid_move(board, col_idx):
    if col_idx is None or col_idx < 0 or col_idx >= COLS:
        return False
    # Check if top cell is empty (column not full)
    return board[0][col_idx] == EMPTY

def drop_token(board, col_idx, token):
    # place from bottom up, return row placed
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == EMPTY:
            board[r][col_idx] = token
            return r
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_four(board, r, c, dr, dc, token):
    # check sequence of 4 starting at (r,c) going (dr,dc)
    for k in range(4):
        rr = r + dr * k
        cc = c + dc * k
        if not in_bounds(rr, cc) or board[rr][cc] != token:
            return False
    return True

def check_win(board, last_r, last_c, token):
    # directions: horiz, vert, diag down-right, diag up-right
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        # To cover all sequences including last move, slide window such that last cell can be pos 0..3
        for offset in range(-3, 1):
            start_r = last_r + dr * offset
            start_c = last_c + dc * offset
            if check_four(board, start_r, start_c, dr, dc, token):
                return True
    return False

def board_full(board):
    # top row has no empties
    return all(cell != EMPTY for cell in board[0])

def get_players():
    n = max(2, min(5, NUM_PLAYERS))
    return list(PLAYER_TOKENS[:n])

def prompt_move(players, current_idx):
    token = players[current_idx]
    while True:
        raw = input("Player {} — choose a column (A-{}): ".format(token, COL_LABELS[-1])).strip()
        if len(raw) != 1:
            print("Please enter one letter from A to {}.".format(COL_LABELS[-1]))
            continue
        col_idx = col_to_index(raw)
        if col_idx is None:
            print("Invalid column. Use A to {}.".format(COL_LABELS[-1]))
            continue
        return col_idx

def main():
    players = get_players()
    board = make_board(ROWS, COLS)
    current_idx = random.randrange(len(players))

    while True:
        print_board(board, players, current_idx)
        col_idx = prompt_move(players, current_idx)
        if not is_valid_move(board, col_idx):
            print("Column {} is full. Press Enter to try again.".format(COL_LABELS[col_idx]))
            input()
            continue

        row_placed = drop_token(board, col_idx, players[current_idx])

        # Check win
        if check_win(board, row_placed, col_idx, players[current_idx]):
            print_board(board, players, current_idx)
            print("Player {} wins!".format(players[current_idx]))
            break

        # Check draw
        if board_full(board):
            print_board(board, players, current_idx)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % len(players)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\nGame interrupted.")
        sys.exit(0)
