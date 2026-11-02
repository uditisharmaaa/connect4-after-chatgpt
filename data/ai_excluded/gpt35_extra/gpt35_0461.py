import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_input(s):
    return len(s) == 1 and 'A' <= s <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*sign
                nc += dc*sign
                if 0<=nr<ROWS and 0<=nc<COLS and board[nr][nc] == checker:
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
        col_letter = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_input(col_letter):
            continue
        col = ord(col_letter) - ord('A')
        row = place_checker(board, col, checker)
        if row == -1:
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
