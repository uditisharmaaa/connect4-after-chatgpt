import os
import random

ROWS = 6
COLS = 7
N_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

players = CHECKERS[:N_PLAYERS]
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        print("| " + " | ".join(board[r]) + " |")
        print("+" + "---+" * COLS)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(sym):
    dirs = [(0,1),(1,0),(1,1),(-1,1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if in_bounds(rr, cc) and board[rr][cc] == sym:
                        cnt += 1
                    else:
                        break
                if cnt == 4:
                    return True
    return False

def board_full():
    for row in board:
        if " " in row:
            return False
    return True

current = random.randint(0, N_PLAYERS - 1)

while True:
    os.system('clear')
    print_board()
    print(f"Player {players[current]}, please enter a column:")
    while True:
        s = input().strip().upper()
        if len(s) == 1 and 'A' <= s <= 'Z':
            col = ord(s) - ord('A')
            if 0 <= col < COLS:
                break
        print("Invalid input. Please enter a valid column letter.")
    if board[0][col] != " ":
        print("Column full. Turn lost. Press Enter to continue.")
        input()
        current = (current + 1) % N_PLAYERS
        continue
    r = ROWS - 1
    while r >= 0 and board[r][col] != " ":
        r -= 1
    board[r][col] = players[current]
    if check_win(players[current]):
        os.system('clear')
        print_board()
        print(f"Player {players[current]} won!")
        break
    if board_full():
        os.system('clear')
        print_board()
        print("Game is a draw.")
        break
    current = (current + 1) % N_PLAYERS
