import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  ", "  ".join([chr(i) for i in range(ord('A'), ord('A') + COLS)]))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_input(current_checker):
    while True:
        col = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(col) == 1 and 'A' <= col <= chr(ord('A') + COLS - 1):
            index = ord(col) - ord('A')
            if board[0][index] == " ":
                return index
            else:
                print("Column is full! What about another column?")
        else:
            print("Invalid column! Please pick a valid letter.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS-3):
            if all(board[row][c] == checker for c in range(col, col+4)):
                return True

    for col in range(COLS):
        for row in range(ROWS-3):
            if all(board[r][col] == checker for r in range(row, row+4)):
                return True

    for row in range(ROWS-3):
        for col in range(COLS-3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLS-3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

board = create_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

while True:
    col = get_input(CHECKERS[current_player])
    place_checker(board, col, CHECKERS[current_player])
    print_board(board)
    if check_win(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    if check_draw(board):
        print("It's a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
