import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    header = "  " + "   ".join(chr(ord('A')+i) for i in range(COLS))
    sep = "+" + "---+"*COLS
    print(header)
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def input_column(player):
    while True:
        c = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if len(c)==1 and 'A' <= c <= chr(ord('A')+COLS-1):
            idx = ord(c)-ord('A')
            return idx
        print("Invalid input. Try again.")

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in [1,-1]:
            rr, cc = r, c
            while True:
                rr += dr*sign
                cc += dc*sign
                if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
                    count +=1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        col = input_column(current_player)
        row = place_checker(board, col, CHECKERS[current_player])
        if row == -1:
            # column full, player loses turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("Game ends in a draw.")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
