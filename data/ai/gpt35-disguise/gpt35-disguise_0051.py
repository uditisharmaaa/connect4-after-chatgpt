import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

board = []
players = CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    global board
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    clear_screen()
    # print column labels
    labels = "  "
    for i in range(COLS):
        labels += chr(ord("A") + i) + "   "
    print(labels)
    # print the board rows with lines
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def valid_column(col):
    if len(col) != 1:
        return False
    c = col.upper()
    if c < 'A' or c >= chr(ord('A') + COLS):
        return False
    return True

def column_index(col):
    return ord(col.upper()) - ord('A')

def is_column_full(c):
    return board[0][c] != " "

def place_checker(c, checker):
    # start from bottom row to top
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r
    return -1 # column full

def check_win(r, c, checker):
    # check directions: horizontal, vertical, two diagonals
    # horizontal
    count = 0
    for col in range(max(0, c - 3), min(COLS, c + 4)):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(max(0, r - 3), min(ROWS, r + 4)):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # diagonal /
    count = 0
    start_row = r + min(3, COLS - 1 - c)
    start_col = c - min(3, COLS - 1 - c)
    # adjust to get start point as top-left of /
    row = start_row
    col = start_col
    while row >= 0 and col < COLS:
        if row < ROWS and board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row -=1
        col +=1
    # diagonal \
    count = 0
    start_row = r - min(3, r)
    start_col = c - min(3, r)
    row = start_row
    col = start_col
    while row < ROWS and col < COLS:
        if row >= 0 and col >= 0 and board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row +=1
        col +=1
    return False

def board_full():
    for c in range(COLS):
        if not is_column_full(c):
            return False
    return True

def main():
    create_board()
    current = random.randint(0, NUM_PLAYERS-1)
    while True:
        print_board()
        print("Player {}, please enter a column:".format(players[current]))
        choice = input().strip().upper()
        if not valid_column(choice):
            # invalid input, ask again
            continue
        c = column_index(choice)
        if is_column_full(c):
            # turn lost
            current = (current +1) % NUM_PLAYERS
            continue
        row_placed = place_checker(c, players[current])
        print_board()
        if check_win(row_placed, c, players[current]):
            print("Player {} won!".format(players[current]))
            break
        if board_full():
            print("It's a draw!")
            break
        current = (current +1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
