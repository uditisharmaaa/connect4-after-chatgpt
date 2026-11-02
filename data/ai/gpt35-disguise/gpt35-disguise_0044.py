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
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+---" * COLS + "+")
        row_str = ""
        for c in range(COLS):
            row_str += "| " + board[r][c] + " "
        row_str += "|"
        print(row_str)
    print("+---" * COLS + "+")

def valid_column(col):
    if len(col) != 1:
        return False
    if not ('A' <= col <= chr(ord('A') + COLS -1)):
        return False
    return True

def place_checker(board, col, checker):
    index = ord(col) - ord('A')
    for r in range(ROWS-1, -1, -1):
        if board[r][index] == " ":
            board[r][index] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal down-left
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True
    return False

def full_board(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        player = players[current]
        print("Player " + player + ", please enter a column:")
        col = input().strip().upper()
        if not valid_column(col):
            continue
        placed = place_checker(board, col, player)
        if not placed:
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, player):
            print("Player " + player + " won!")
            break
        if full_board(board):
            print("It is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
