import os
import random

ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # For 2 players only, extendable to more players

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:
            col_index = ord(column) - 65
            if board[0][col_index] == " ":
                return col_index
        print("Invalid input. Please try again.")

def place_checker(column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_winner(checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw():
    return all(board[0][col] != " " for col in range(COLS))

# Game initialization
board = initialize_board()
current_player = random.choice(PLAYERS)

# Game loop
while True:
    print_board(board)
    column = get_valid_input(current_player)
    if place_checker(column, current_player):
        if check_winner(current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw():
            print_board(board)
            print("The game is a draw!")
            break
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
    else:
        print("Column is full. Please choose another column.")
