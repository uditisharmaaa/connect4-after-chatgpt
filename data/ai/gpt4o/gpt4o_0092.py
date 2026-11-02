import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column_choice):
    return column_choice.isalpha() and column_choice.isupper() and ord(column_choice) - 65 < COLUMNS

def is_column_full(board, column):
    return board[0][column] != " "

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_win_condition(board, checker):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal Checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(row[0] != " " for row in board)

def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        column_choice = input().strip()
        
        # Validate input
        if not is_valid_column(column_choice):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(column_choice) - 65

        if is_column_full(board, column):
            print("Column is full. Please choose another column.")
            continue

        place_checker(board, column, current_checker)
        print_board(board)

        if check_win_condition(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Alternate turns
        current_player_index = (current_player_index + 1) % PLAYERS

play_game()
