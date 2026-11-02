import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def input_column(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if len(col) != 1 or not ('A' <= col <= chr(ord('A') + COLS -1)):
            continue
        return ord(col) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, ch):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            rr, cc = r, c
            while True:
                rr += dr * sign
                cc += dc * sign
                if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == ch:
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
    current = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        col = input_column(players[current])
        r = place_checker(board, col, players[current])
        if r == -1:
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, r, col, players[current]):
            print(f"Player {players[current]} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
