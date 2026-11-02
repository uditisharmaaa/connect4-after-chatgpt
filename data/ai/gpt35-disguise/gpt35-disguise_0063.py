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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for i in range(COLS):
        print(" " + letters[i] + "  ", end="")
    print()
    line = "+---"*COLS + "+"
    for r in range(ROWS):
        print(line)
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print(line)

def valid_input(s):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(s) != 1:
        return False
    if s not in letters[:COLS]:
        return False
    return True

def column_full(board, col):
    if board[0][col] != " ":
        return True
    return False

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # horizontal check
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # vertical check
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count=0

    # diagonal \ check
    start_r = row
    start_c = col
    while start_r >0 and start_c >0:
        start_r -=1
        start_c -=1
    count=0
    r = start_r
    c = start_c
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count=0
        r +=1
        c +=1

    # diagonal / check
    start_r = row
    start_c = col
    while start_r < ROWS-1 and start_c >0:
        start_r +=1
        start_c -=1
    count=0
    r = start_r
    c = start_c
    while r >=0 and c < COLS:
        if board[r][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count=0
        r -=1
        c +=1

    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randrange(PLAYERS)
    print_board(board)
    while True:
        print("Player {}, please enter a column:".format(players[current]), end=" ")
        move = input().strip().upper()
        if not valid_input(move):
            continue
        col = ord(move) - ord('A')
        if col <0 or col >= COLS:
            continue
        if column_full(board, col):
            # turn lost
            current = (current +1) % PLAYERS
            continue
        row_placed = place_checker(board, col, players[current])
        print_board(board)
        if check_win(board, row_placed, col, players[current]):
            print("Player {} won!".format(players[current]))
            break
        if board_full(board):
            print("Draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
