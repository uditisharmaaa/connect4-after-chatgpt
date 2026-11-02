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
    letters = ""
    for c in range(COLS):
        letters += "  " + chr(ord('A') + c) + " "
    print(letters)
    print("+---" * COLS + "+")
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
        print("+---" * COLS + "+")

def is_valid_column(col):
    if len(col) != 1:
        return False
    if not ('A' <= col <= chr(ord('A') + COLS - 1)):
        return False
    return True

def column_has_space(board, col):
    c = ord(col) - ord('A')
    return board[0][c] == " "

def place_checker(board, col, checker):
    c = ord(col) - ord('A')
    for r in reversed(range(ROWS)):
        if board[r][c] == " ":
            board[r][c] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c]==checker and board[r][c+1]==checker and board[r][c+2]==checker and board[r][c+3]==checker:
                return True
    # vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c]==checker and board[r+1][c]==checker and board[r+2][c]==checker and board[r+3][c]==checker:
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c]==checker and board[r+1][c+1]==checker and board[r+2][c+2]==checker and board[r+3][c+3]==checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c]==checker and board[r-1][c+1]==checker and board[r-2][c+2]==checker and board[r-3][c+3]==checker:
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    while True:
        print_board(board)
        print("Player " + players[current] + ", please enter a column:")
        move = input()
        move = move.strip().upper()
        if not is_valid_column(move):
            continue
        if not column_has_space(board, move):
            # lose turn if column full
            current = (current + 1) % PLAYERS
            continue
        placed = place_checker(board, move, players[current])
        if placed:
            if check_win(board, players[current]):
                print_board(board)
                print("Player " + players[current] + " won!")
                break
            if check_draw(board):
                print_board(board)
                print("Draw!")
                break
            current = (current + 1) % PLAYERS
        else:
            current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
