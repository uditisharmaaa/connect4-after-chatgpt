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
    line = "+---" * COLS + "+"
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def valid_column(inp):
    if len(inp) != 1:
        return False
    if not ('A' <= inp <= chr(ord('A') + COLS - 1)):
        return False
    return True

def get_column_index(inp):
    return ord(inp) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def check_line(line, checker):
    count = 0
    for ch in line:
        if ch == checker:
            count +=1
            if count >=4:
                return True
        else:
            count=0
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        line = board[r]
        if check_line(line, checker):
            return True
    # vertical
    for c in range(COLS):
        line = []
        for r in range(ROWS):
            line.append(board[r][c])
        if check_line(line, checker):
            return True
    # diagonal top-left to bottom-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            line = [board[r+i][c+i] for i in range(4)]
            if all(ch == checker for ch in line):
                return True
    # diagonal bottom-left to top-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            line = [board[r-i][c+i] for i in range(4)]
            if all(ch == checker for ch in line):
                return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        print("Player {}, please enter a column:".format(checker))
        inp = input().strip().upper()
        if not valid_column(inp):
            continue
        col = get_column_index(inp)
        if not place_checker(board, col, checker):
            # col full, lose turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker):
            print("Player {} won!".format(checker))
            break
        if board_full(board):
            print("Draw!")
            break
        current = (current + 1) % PLAYERS


if __name__ == "__main__":
    main()
