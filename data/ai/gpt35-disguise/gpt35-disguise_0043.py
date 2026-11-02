import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    # print column labels
    labels = ""
    for i in range(COLS):
        labels += "  " + chr(ord('A') + i) + " "
    print(labels)
    # print board rows
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        rowline = "|"
        for c in range(COLS):
            rowline += " " + board[r][c] + " |"
        print(rowline)
    print(line)

def valid_input(s):
    if len(s) != 1:
        return False
    if not ('A' <= s <= chr(ord('A') + COLS -1)):
        return False
    return True

def place_checker(board, col, checker):
    # place checker in lowest empty spot in column col
    # col is index 0 based
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right check
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal down-left check
    for r in range(ROWS-3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    while True:
        clear()
        print_board(board)
        print("Player " + players[current] + ", please enter a column:")
        inp = input().strip().upper()
        if not valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        if not place_checker(board, col, players[current]):
            # full column, lose turn
            current = (current + 1) % PLAYERS
            continue
        if check_win(board, players[current]):
            clear()
            print_board(board)
            print("Player " + players[current] + " won!")
            break
        if board_full(board):
            clear()
            print_board(board)
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
