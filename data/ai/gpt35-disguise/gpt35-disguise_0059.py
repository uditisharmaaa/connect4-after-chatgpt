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
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = ""
    for i in range(COLS):
        letters += "  " + chr(ord("A") + i) + " "
    print(letters)
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            row_str += "| " + board[r][c] + " "
        row_str += "|"
        print(row_str)
        print("+---" * COLS + "+")

def get_player_input(player):
    while True:
        col = input("Player {}, please enter a column: ".format(CHECKERS[player]))
        if len(col) != 1:
            continue
        if not col.isalpha():
            continue
        col = col.upper()
        if ord(col) < ord("A") or ord(col) >= ord("A") + COLS:
            continue
        return ord(col) - ord("A")

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, r, c, checker):
    # Check horizontal
    count = 0
    for col in range(max(0, c-3), min(COLS, c+4)):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for row in range(max(0, r-3), min(ROWS, r+4)):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    # Check diagonal top-left to bottom-right
    count = 0
    start_offset = min(3, r, c)
    start_r = r - start_offset
    start_c = c - start_offset
    while start_r < 0 or start_c < 0:
        if start_r < 0:
            start_r += 1
        if start_c < 0:
            start_c += 1
    for i in range(WIN_COUNT+3):
        rr = start_r + i
        cc = start_c + i
        if rr >= ROWS or cc >= COLS:
            break
        if board[rr][cc] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    # Check diagonal bottom-left to top-right
    count = 0
    start_offset = min(3, ROWS - 1 - r, c)
    start_r = r + start_offset
    start_c = c - start_offset
    for i in range(WIN_COUNT+3):
        rr = start_r - i
        cc = start_c + i
        if rr < 0 or cc >= COLS:
            break
        if board[rr][cc] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        col = get_player_input(current_player)
        r, c = place_checker(board, col, CHECKERS[current_player])
        if r == -1:
            print("Column full, you lose your turn!")
        else:
            print_board(board)
            if check_win(board, r, c, CHECKERS[current_player]):
                print("Player {} won!".format(CHECKERS[current_player]))
                break
            if board_full(board):
                print("The game is a draw.")
                break
        current_player = (current_player + 1) % PLAYERS

main()
