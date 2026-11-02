import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def is_valid_input(input_char, columns):
    return input_char in (chr(65 + i) for i in range(columns))

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal /
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(range(PLAYERS))
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip().upper()
        if not is_valid_input(user_input, COLUMNS):
            continue
        column = ord(user_input) - ord('A')
        if place_checker(board, column, CHECKERS[current_player]):
            if check_winner(board, CHECKERS[current_player]):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw.")
                break
            current_player = (current_player + 1) % PLAYERS

play_game()
