import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '   ' + '   '.join(COLUMN_LABELS)
    separator = '+---' * COLUMNS + '+'
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_input(input_char):
    return input_char in COLUMN_LABELS

def is_column_full(board, column):
    return board[0][column] != ' '

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_for_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            column_input = input().strip()
            if is_valid_input(column_input):
                column_index = COLUMN_LABELS.index(column_input)
                if not is_column_full(board, column_index):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a valid column letter.")

        place_checker(board, column_index, current_checker)
        print_board(board)

        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

play_game()
