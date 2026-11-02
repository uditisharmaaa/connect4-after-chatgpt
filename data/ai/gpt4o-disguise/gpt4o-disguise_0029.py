import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
FIRST_PLAYER = random.randint(0, MAX_PLAYERS - 1)

# Initialize the board
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return column.isalpha() and 'A' <= column <= chr(64 + COLUMNS)

def is_valid_move(column):
    col_index = ord(column.upper()) - 65
    return board[0][col_index] == ' '

def place_checker(player, column):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = CHECKERS[player]
            break

def check_winner(player):
    checker = CHECKERS[player]
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
               (c + 3 < COLUMNS and r + 3 < ROWS and all(board[r + i][c + i] == checker for i in range(4))) or \
               (c - 3 >= 0 and r + 3 < ROWS and all(board[r + i][c - i] == checker for i in range(4))):
                return True
    return False

def is_draw():
    return all(board[0][c] != ' ' for c in range(COLUMNS))

current_player = FIRST_PLAYER

while True:
    print_board()
    move_valid = False
    
    while not move_valid:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if is_valid_input(column) and is_valid_move(column):
            place_checker(current_player, column)
            move_valid = True
        else:
            print("Invalid move, try again.")

    if check_winner(current_player):
        print_board()
        print(f"Player {CHECKERS[current_player]} won!")
        break
    elif is_draw():
        print_board()
        print("The game is a draw!")
        break

    current_player = (current_player + 1) % MAX_PLAYERS
