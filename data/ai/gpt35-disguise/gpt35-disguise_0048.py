import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+---" * COLS + "+")
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+---" * COLS + "+")

def is_valid_column(col):
    if len(col) != 1:
        return False
    if not ('A' <= col <= chr(ord('A') + COLS -1)):
        return False
    return True

def column_index(col):
    return ord(col) - ord('A')

def place_checker(board, col, checker):
    c = column_index(col)
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r, c
    return -1, -1

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count +=1
                if count >=4:
                    return True
            else:
                count = 0
    # vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count +=1
                if count >=4:
                    return True
            else:
                count = 0
    # diagonal down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def is_board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        print("Player " + CHECKERS[current_player] + ", please enter a column:")
        inp = input().strip().upper()
        if not is_valid_column(inp):
            continue
        
        r, c = place_checker(board, inp, CHECKERS[current_player])
        if r == -1:
            current_player = (current_player +1) % PLAYERS
            continue

        print_board(board)
        if check_win(board, CHECKERS[current_player]):
            print("Player " + CHECKERS[current_player] + " won!")
            break

        if is_board_full(board):
            print("It's a draw!")
            break

        current_player = (current_player +1) % PLAYERS

if __name__ == "__main__":
    main()
