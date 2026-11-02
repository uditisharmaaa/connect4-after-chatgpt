import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+"*COLS)

def input_column(player):
    while True:
        col = input("Player {}, please enter a column: ".format(player)).strip().upper()
        if len(col) != 1:
            continue
        if col < 'A' or col >= chr(ord('A')+COLS):
            continue
        return ord(col)-ord('A')

def place_checker(board, col, checker):
    # The checker falls to the lowest empty position in that column
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1  # column full

def check_win(board, row, col, checker):
    # check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # check diagonal (top-left to bottom-right)
    start_r = row
    start_c = col
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    count = 0
    r = start_r
    c = start_c
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r += 1
        c += 1
    # check diagonal (bottom-left to top-right)
    start_r = row
    start_c = col
    while start_r < ROWS-1 and start_c > 0:
        start_r += 1
        start_c -= 1
    count = 0
    r = start_r
    c = start_c
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current_player]
        col = input_column(checker)
        row = place_checker(board, col, checker)
        if row == -1:
            # full column, lose turn
            print("Column full, you lose the turn.")
        else:
            print_board(board)
            if check_win(board, row, col, checker):
                print("Player {} won!".format(checker))
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS

main()
