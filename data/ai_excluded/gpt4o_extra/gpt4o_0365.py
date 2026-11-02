import os
import random

# Constants for the game setup
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))]))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_input():
    while True:
        player_input = input().strip().upper()
        if player_input.isalpha() and 'A' <= player_input < chr(ord('A') + COLS):
            return ord(player_input) - ord('A')
        print("Invalid input. Please enter a valid column letter:")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLS - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == checker:
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == checker:
                return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
        for col in range(3, COLS):
            if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == checker:
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4():
    board = initialize_board(ROWS, COLS)
    current_player = random.choice(PLAYERS)
    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        col = get_valid_input()
        if place_checker(board, col, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")

connect4()
