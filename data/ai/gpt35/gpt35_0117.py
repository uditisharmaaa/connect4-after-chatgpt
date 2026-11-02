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
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    line = "+---"*COLS + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def valid_input(col):
    return len(col) == 1 and 'A' <= col <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    col_idx = ord(col) - ord('A')
    for r in reversed(range(ROWS)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    # diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
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
        if not valid_input(col):
            continue
        if not place_checker(board, col, checker):
            # full column, turn lost
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
