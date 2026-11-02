import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return column.isalpha() and 'A' <= column < chr(ord('A') + COLUMNS)

def player_input():
    while True:
        inp = input("Please enter a column: ")
        if is_valid_input(inp):
            col_index = ord(inp.upper()) - ord('A')
            if board[0][col_index] == " ":
                return col_index
        print("Invalid input, try again.")

def place_checker(board, checker, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            break

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS - 4 and all(board[row][col+i] == checker for i in range(4))) or \
               (row <= ROWS - 4 and all(board[row+i][col] == checker for i in range(4))) or \
               (row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row+i][col+i] == checker for i in range(4))) or \
               (row <= ROWS - 4 and col >= 3 and all(board[row+i][col-i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

board = create_board()
print_board(board)
current_player = random.choice(range(PLAYERS))

while True:
    print_board(board)
    print(f"Player {CHECKERS[current_player]}")
    col = player_input()
    place_checker(board, CHECKERS[current_player], col)
    
    if check_win(board, CHECKERS[current_player]):
        print_board(board)
        print(f"Player {CHECKERS[current_player]} won!")
        break
        
    if check_draw(board):
        print_board(board)
        print("Game is a draw!")
        break

    current_player = (current_player + 1) % PLAYERS
