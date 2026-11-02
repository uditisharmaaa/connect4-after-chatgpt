import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
CHECKERS = CHECKERS[:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_player_input(current_player):
    while True:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= 'A' + chr(COLS - 1):
            column = ord(column) - 65
            if board[0][column] == ' ':
                return column
            else:
                print("Column is full! Choose another.")
        else:
            print("Invalid input! Enter one of A-G.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if c <= COLS - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            if c <= COLS - 4 and r <= ROWS - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if c >= 3 and r <= ROWS - 4 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

board = create_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

while True:
    col = get_player_input(current_player)
    place_checker(board, col, CHECKERS[current_player])
    print_board(board)

    if check_win(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    elif check_draw(board):
        print("It's a draw!")
        break

    current_player = (current_player + 1) % PLAYERS
