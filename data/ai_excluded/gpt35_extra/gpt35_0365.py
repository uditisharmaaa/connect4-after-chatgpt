import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_col(col):
    return len(col) == 1 and 'A' <= col <= chr(64+COLS)

def col_full(board, c):
    return all(board[r][c] != " " for r in range(ROWS))

def place_checker(board, c, checker):
    for r in reversed(range(ROWS)):
        if board[r][c] == " ":
            board[r][c] = checker
            return r
    return -1

def check_win(board, r, c, ch):
    def count(delta_r, delta_c):
        cnt = 0
        rr, cc = r + delta_r, c + delta_c
        while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == ch:
            cnt += 1
            rr += delta_r
            cc += delta_c
        return cnt

    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        if 1 + count(dr, dc) + count(-dr, -dc) >= WIN_LEN:
            return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[turn]
        col = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not valid_col(col):
            continue
        c = ord(col) - 65
        if col_full(board, c):
            # Lose turn if column full
            turn = (turn + 1) % PLAYERS
            continue
        r = place_checker(board, c, checker)
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
