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
    clear()
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---" * COLS + "+")

def valid_column(col_str):
    if len(col_str) != 1:
        return False
    c = ord(col_str)
    if c < ord('A') or c >= ord('A') + COLS:
        return False
    return True

def column_index(col_str):
    return ord(col_str) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
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

    print_board(board)

    while True:
        player = players[current]
        print("Player " + player + ", please enter a column:")
        col_input = input().strip().upper()
        if not valid_column(col_input):
            print("Invalid input. Try again.")
            continue
        col = column_index(col_input)
        if not place_checker(board, col, player):
            print("Column full. You lose your turn.")
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, player):
            print("Player " + player + " won!")
            break
        if board_full(board):
            print("Draw!")
            break
        current = (current + 1) % PLAYERS

main()
