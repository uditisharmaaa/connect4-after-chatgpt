import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    line = "+" + ("---+" * len(board[0]))
    for r in range(len(board)):
        print(line)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(line)

def get_col_input(max_cols, player):
    while True:
        s = input(f"Player {player}, please enter a column: ").strip()
        if len(s) != 1:
            continue
        ch = s.upper()
        if not ('A' <= ch <= 'Z'):
            continue
        col = ord(ch) - ord('A')
        if 0 <= col < max_cols:
            return col

def place(board, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r, col
    return None

def check_win(board, sym):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            if c <= COLS - 4 and all(board[r][c + k] == sym for k in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r + k][c] == sym for k in range(4)):
                return True
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + k][c + k] == sym for k in range(4)):
                return True
            if r >= 3 and c <= COLS - 4 and all(board[r - k][c + k] == sym for k in range(4)):
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    players = CHECKERS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        col = get_col_input(COLS, players[current])
        pos = place(board, col, players[current])
        if pos is None:
            current = (current + 1) % NUM_PLAYERS
            continue
        if check_win(board, players[current]):
            print_board(board)
            print(f"Player {players[current]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("Draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
