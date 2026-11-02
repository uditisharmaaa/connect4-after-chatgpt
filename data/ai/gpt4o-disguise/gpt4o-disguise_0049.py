import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]  # Change for more players

# Initialize the board
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_move(column):
    return column >= 0 and column < COLUMNS and board[0][column] == " "

def make_move(player, column):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            break

def check_winner(player):
    # Check horizontal, vertical, and diagonals for win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
                
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True
    
    return False

def check_draw():
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    current_player = random.choice(PLAYERS)
    while True:
        print_board()
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            move = input().upper()
            if len(move) == 1 and move.isalpha():
                col = ord(move) - 65
                if is_valid_move(col):
                    break
            print("Invalid input, please enter a column:")
        
        make_move(current_player, col)
        
        if check_winner(current_player):
            print_board()
            print(f"Player {current_player} won!")
            break
        elif check_draw():
            print_board()
            print("The game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

play_game()
