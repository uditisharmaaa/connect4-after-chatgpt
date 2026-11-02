import os
import random

# Constants for the game setup
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def print_board(board):
    os.system('clear')
    column_labels = ' '.join([chr(ord('A') + i) for i in range(COLUMNS)])
    print(f"  {column_labels}")
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def get_valid_input():
    while True:
        user_input = input().strip().upper()
        if user_input.isalpha() and 'A' <= user_input <= chr(ord('A') + COLUMNS - 1):
            return ord(user_input) - ord('A')
        else:
            print("Invalid input. Please enter a valid column:")

def drop_checker(board, checker, column):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
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
    return all(cell != ' ' for row in board for cell in row)

def connect_four():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = get_valid_input()
        if drop_checker(board, CHECKERS[current_player], column):
            print_board(board)
            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break

            # Switch to the next player
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. Player loses the turn.")

if __name__ == "__main__":
    connect_four()
