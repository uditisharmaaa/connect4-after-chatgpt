import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_column(col):
    return col.isalpha() and 'A' <= col <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    c = ord(col) - ord('A')
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r, c
    return -1, -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for s in [1,-1]:
            rr, cc = r, c
            while True:
                rr += dr*s
                cc += dc*s
                if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        col = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_column(col):
            continue
        r, c = place_checker(board, col, checker)
        if r == -1:  # Column full, lose turn
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current = (current + 1) % PLAYERS

if __name__=="__main__":
    main()
