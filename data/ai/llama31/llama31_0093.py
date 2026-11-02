import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = "XOVHM"

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + " ".join(string.ascii_uppercase[:COLUMNS]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(input_str, board):
    if not input_str.isalpha():
        return False
    if len(input_str)!= 1:
        return False
    column = ord(input_str.upper()) - ord('A')
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column]!= " ":
        return False
    return True

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for i in range(len(board) - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(COLUMNS - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(COLUMNS - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    return all([cell!= " " for row in board for cell in row])

def game():
    board = create_board()
    players = list(CHECKERS[:PLAYERS])
    current_player = random.choice(players)
    while True:
        print_board(board)
        input_str = input(f"Player {current_player}, please enter a column: ")
        if not is_valid_input(input_str, board):
            continue
        column = ord(input_str.upper()) - ord('A')
        place_checker(board, column, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

game()
