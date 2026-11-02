import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    line = "+" + "---+"*COLS
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def input_column(player):
    while True:
        c = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if len(c) != 1 or not ('A' <= c <= chr(ord('A') + COLS - 1)):
            print("Invalid input. Try again.")
        else:
            return ord(c) - ord('A')

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
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0<=nr<ROWS and 0<=nc<COLS and board[nr][nc]==ch:
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
    current = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        col = input_column(current)
        row = place_checker(board, col, players[current])
        if row == -1:
            print("Column full, turn lost.")
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, row, col, players[current]):
            print(f"Player {players[current]} won!")
            break
        if board_full(board):
            print("Game is a draw.")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
