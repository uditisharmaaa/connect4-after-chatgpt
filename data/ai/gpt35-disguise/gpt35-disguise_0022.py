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
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    line = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def is_valid_column(col):
    if len(col) != 1:
        return False
    if not ('A' <= col <= chr(ord('A') + COLS -1)):
        return False
    return True

def is_column_full(board, col_index):
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index

def check_win(board, row, col, checker):
    # horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
    # vertical
    count =0
    for r in range(ROWS):
        if board[r][col] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
    # diagonal /
    count = 0
    start_row = row
    start_col = col
    while start_row >0 and start_col < COLS -1:
        start_row -=1
        start_col +=1
    r = start_row
    c = start_col
    while r < ROWS and c >=0:
        if board[r][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count = 0
        r +=1
        c -=1
    # diagonal \
    count =0
    start_row = row
    start_col = col
    while start_row >0 and start_col >0:
        start_row -=1
        start_col -=1
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
        r +=1
        c +=1
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    current = random.randint(0, PLAYERS -1)
    player_checkers = CHECKERS[:PLAYERS]
    print_board(board)
    while True:
        player = player_checkers[current]
        print("Player {}, please enter a column:".format(player))
        col = input().strip().upper()
        if not is_valid_column(col):
            continue
        col_index = ord(col) - ord('A')
        if is_column_full(board, col_index):
            # loses turn
            current = (current +1) % PLAYERS
            continue
        row, col_placed = place_checker(board, col_index, player)
        print_board(board)
        if check_win(board, row, col_placed, player):
            print("Player {} won!".format(player))
            break
        if is_draw(board):
            print("Draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
