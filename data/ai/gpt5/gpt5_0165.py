import os
import random
import string

# Configuration (changeable, but submission should be 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LEN = 4

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows, cols = len(board), len(board[0])
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    sep = "+" + ("---+" * cols)
    print(header)
    print(sep)
    for r in range(rows):
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
        print(sep)

def get_column_input(cols, current_token):
    valid_letters = set(string.ascii_uppercase[:cols])
    while True:
        try:
            s = input(f"Player {current_token}, please enter a column: ").strip()
        except EOFError:
            continue
        if len(s) == 1 and s.upper() in valid_letters:
            return string.ascii_uppercase.index(s.upper())
        # invalid input, ask again

def drop_checker(board, col, token):
    # returns row index if placed, else None if column full
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, last_r, last_c, token):
    if last_r is None:  # no move made
        return False
    rows, cols = len(board), len(board[0])
    directions = [(0,1),(1,0),(1,1),(-1,1)]
    for dr, dc in directions:
        count = 1
        # forward
        r, c = last_r+dr, last_c+dc
        while in_bounds(r,c,rows,cols) and board[r][c] == token:
            count += 1
            r += dr; c += dc
        # backward
        r, c = last_r-dr, last_c-dc
        while in_bounds(r,c,rows,cols) and board[r][c] == token:
            count += 1
            r -= dr; c -= dc
        if count >= WIN_LEN:
            return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

def main():
    assert 2 <= NUM_PLAYERS <= 5
    assert 1 <= COLS <= 26
    board = create_board(ROWS, COLS)
    current_idx = random.randrange(NUM_PLAYERS)
    clear()
    print_board(board)
    while True:
        token = TOKENS[current_idx]
        col = get_column_input(COLS, token)
        row_placed = drop_checker(board, col, token)
        clear()
        print_board(board)
        if row_placed is None:
            # column full, lose the turn (no retry)
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue
        if check_win(board, row_placed, col, token):
            print(f"Player {token} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
