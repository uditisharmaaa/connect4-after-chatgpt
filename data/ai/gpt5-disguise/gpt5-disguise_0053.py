import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ['X', 'O', 'V', 'H', 'M']

def make_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    header = '  ' + '   '.join(letters)
    sep = '+' + '---+' * len(b[0])
    print(header)
    print(sep)
    for r in range(len(b)):
        row = '|'
        for c in range(len(b[0])):
            row += ' ' + b[r][c] + ' |'
        print(row)
        print(sep)

def clear():
    os.system('clear')

def lowest_empty_row(b, col):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == ' ':
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, token):
    rows = len(b)
    cols = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != token:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < 4 and in_bounds(rr, cc, rows, cols) and b[rr][cc] == token:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == 4:
                    return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == ' ':
                return False
    return True

def main():
    players = TOKENS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear()
        print_board(board)
        current = players[turn]
        col_input = ''
        while True:
            col_input = input(f"Player {current}, please enter a column: ").strip().upper()
            if len(col_input) != 1 or not col_input.isalpha():
                print("Invalid input.")
                continue
            col_idx = ord(col_input) - ord('A')
            if col_idx < 0 or col_idx >= COLS:
                print("Column out of range.")
                continue
            break

        row_idx = lowest_empty_row(board, col_idx)
        if row_idx is None:
            print("Column is full. Turn lost.")
            input("Press Enter to continue...")
            turn = (turn + 1) % NUM_PLAYERS
            continue

        board[row_idx][col_idx] = current

        if check_win(board, current):
            clear()
            print_board(board)
            print(f"Player {current} won!")
            break

        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break

        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
