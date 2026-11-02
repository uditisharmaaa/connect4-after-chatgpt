import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O']

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def get_first_player():
    return random.randint(0, PLAYERS - 1)

def get_valid_input():
    while True:
        col = input("Player {}, please enter a column: ".format(CHECKERS[current_player])).upper()
        if len(col) == 1 and 'A' <= col <= chr(ord('A') + COLS - 1):
            col_index = ord(col) - ord('A')
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full!")
        else:
            print("Invalid input! Please enter a valid column.")

def place_checker(col):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = CHECKERS[current_player]
            break
        
def check_winner():
    # Horizontal Check
    for row in board:
        for col in range(COLS - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] != ' ':
                return True
    # Vertical Check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] != ' ':
                return True
    # Diagonal (descending) Check
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] != ' ':
                return True
    # Diagonal (ascending) Check
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] != ' ':
                return True
    return False

def check_draw():
    return all(board[0][col] != ' ' for col in range(COLS))

board = create_board()
current_player = get_first_player()
print_board(board)

while True:
    col = get_valid_input()
    place_checker(col)
    print_board(board)
    if check_winner():
        print("Player {} won!".format(CHECKERS[current_player]))
        break
    if check_draw():
        print("The game is a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
