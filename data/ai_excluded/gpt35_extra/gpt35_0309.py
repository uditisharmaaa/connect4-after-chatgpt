import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS+"+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS+"+")

def valid_input(col):
    return len(col) == 1 and 'A' <= col <= chr(ord('A')+COLS-1)

def column_index(col):
    return ord(col) - ord('A')

def place_checker(board, col_idx, checker):
    for r in reversed(range(ROWS)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r
    return -1  # full column

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for dir in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*dir; nc += dc*dir
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                    count += 1
                    if count >=4:
                        return True
                else:
                    break
    return False

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[turn]
        inp = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_input(inp):
            continue
        col = column_index(inp)
        row = place_checker(board, col, checker)
        if row == -1: 
            turn = (turn + 1) % PLAYERS  # lose turn on full column
        else:
            print_board(board)
            if check_win(board, row, col, checker):
                print(f"Player {checker} won!")
                break
            if full_board(board):
                print("Draw!")
                break
            turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
