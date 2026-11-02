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
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(COLS):
        labels += "  " + chr(ord('A') + i) + " "
    print(labels)
    # Print board
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    line = "+"
    for c in range(COLS):
        line += "---+"
    print(line)

def valid_input(s):
    if len(s) != 1:
        return False
    if s < 'A' or s >= chr(ord('A') + COLS):
        return False
    return True

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    # Check horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # Check vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # Check diagonal /
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c < COLS-1:
        start_r -=1
        start_c +=1
    rr = start_r
    cc = start_c
    while rr < ROWS and cc >=0:
        if board[rr][cc] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count=0
        rr +=1
        cc -=1
    # Check diagonal \
    count =0
    start_r = r
    start_c = c
    while start_r > 0 and start_c >0:
        start_r -=1
        start_c -=1
    rr = start_r
    cc = start_c
    while rr < ROWS and cc < COLS:
        if board[rr][cc] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
        rr +=1
        cc +=1
    return False

def check_draw(board):
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
        if not valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        if is_column_full(board, col):
            # turn lost
            current = (current +1)%PLAYERS
            print_board(board)
            continue
        row = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, row, col, checker):
            print("Player {} won!".format(checker))
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current = (current +1)%PLAYERS

if __name__ == "__main__":
    main()
