import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear():
    os.system('clear')

def print_board():
    clear()
    # print top letters
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    # print board
    for r in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(ch):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if ch not in letters[:COLS]:
        return False
    col = letters.index(ch)
    # if top row on that col is not empty means full col
    if board[0][col] != " ":
        return False
    return True

def place_checker(col, checker):
    # place from bottom up
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # if full return None (should not happen if we check input)
    return None

def check_win(r, c, checker):
    # directions: horizontal, vertical, diagonal /
    directions = [
        [(0,1), (0,-1)],
        [(1,0), (-1,0)],
        [(1,1), (-1,-1)],
        [(1,-1), (-1,1)]
    ]
    for dir_pair in directions:
        count = 1
        for dr, dc in dir_pair:
            rr, cc = r, c
            while True:
                rr += dr
                cc += dc
                if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
                    break
                if board[rr][cc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full():
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)

    print_board()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    while True:
        ch = players[current]
        print("Player " + ch + ", please enter a column:")
        inp = input()
        inp = inp.strip().upper()

        if not is_valid_column(inp):
            # if invalid input or full column, lose turn only if column full
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if inp in letters[:COLS]:
                col_check = letters.index(inp)
                if board[0][col_check] != " ":
                    # full column, lose turn
                    current = (current + 1) % PLAYERS
                    print_board()
                    continue
            # invalid input, ask again
            continue

        col = letters.index(inp)
        pos = place_checker(col, ch)
        print_board()
        r, c = pos

        if check_win(r,c,ch):
            print("Player " + ch + " won!")
            break

        if board_full():
            print("The game is a draw.")
            break

        current = (current + 1) % PLAYERS

main()
