import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" " for _ in range(COLS)]
        board.append(row)
    return board

def print_board(board):
    letters = [chr(ord('A')+i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+---"*COLS + "+")
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+---"*COLS + "+")

def valid_input(s):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    col = ord(s) - ord('A')
    if col < 0 or col >= COLS:
        return False
    return True

def place_checker(board, col, checker):
    # from bottom row up
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # diagonal down right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # diagonal up right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

board = create_board()

players = CHECKERS[:PLAYERS]
curr = random.randint(0, PLAYERS-1)

clear_screen()
print_board(board)

while True:
    checker = players[curr]
    print("Player " + checker + ", please enter a column:")
    col_in = input().strip().upper()
    if not valid_input(col_in):
        continue
    col = ord(col_in) - ord('A')
    placed = place_checker(board, col, checker)
    if not placed:
        # lose turn if column full
        curr = (curr + 1) % PLAYERS
        clear_screen()
        print_board(board)
        continue
    clear_screen()
    print_board(board)
    if check_win(board, checker):
        print("Player " + checker + " won!")
        break
    if board_full(board):
        print("Game is a draw!")
        break
    curr = (curr + 1) % PLAYERS
