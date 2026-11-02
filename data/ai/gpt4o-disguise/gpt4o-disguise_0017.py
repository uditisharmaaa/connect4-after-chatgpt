import random
import os

COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
players = CHECKERS[:NUM_PLAYERS]
current_player = random.choice(players)

def print_board():
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+---+---+---+---+---+---+")

def is_valid_move(column):
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == ' '

def place_checker(column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return

def check_win():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != ' ' and (
               check_direction(row, col, 0, 1) or
               check_direction(row, col, 1, 0) or
               check_direction(row, col, 1, 1) or
               check_direction(row, col, 1, -1)):
                return True
    return False

def check_direction(row, col, dr, dc):
    checker = board[row][col]
    for i in range(1, 4):
        r = row + dr * i
        c = col + dc * i
        if r < 0 or r >= ROWS or c < 0 or c >= COLS or board[r][c] != checker:
            return False
    return True

def check_draw():
    for row in board:
        if ' ' in row:
            return False
    return True

while True:
    print_board()
    col_input = input(f"Player {current_player}, please enter a column: ")
    try:
        col_index = ord(col_input.upper()) - ord('A')
        if not is_valid_move(col_index):
            continue
        place_checker(col_index, current_player)
        if check_win():
            print_board()
            print(f"Player {current_player} won!")
            break
        if check_draw():
            print_board()
            print("The game is a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]
    except:
        continue
