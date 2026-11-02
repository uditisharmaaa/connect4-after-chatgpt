import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" + "---+" * (COLUMNS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLUMNS - 1) + "---+")

def get_valid_column_input(player):
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").strip().upper()
        if len(column) == 1 and 'A' <= column <= 'G':
            column_index = ord(column) - 65
            if is_column_valid(column_index):
                return column_index
            else:
                print("Column is full, please try another one.")
        else:
            print("Invalid input. Please enter a letter from A to G.")

def is_column_valid(column):
    return board[0][column] == " "

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board):
    # Check horizontal, vertical, and diagonal lines for a win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] != " " and all(board[row][col] == board[row][col + i] for i in range(4)):
                return True

    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] != " " and all(board[row][col] == board[row + i][col] for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] != " " and all(board[row][col] == board[row + i][col + i] for i in range(4)):
                return True
            
            if board[row][col + 3] != " " and all(board[row][col + 3] == board[row + i][col + 3 - i] for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Initialize the game
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)

# Main game loop
while True:
    print_board(board)
    current_player = PLAYERS[current_player_index]
    column = get_valid_column_input(current_player)
    drop_checker(board, column, current_player)

    if check_winner(board):
        print_board(board)
        print(f"Player {current_player} won!")
        break
    elif check_draw(board):
        print_board(board)
        print("The game is a draw!")
        break

    current_player_index = (current_player_index + 1) % len(PLAYERS)
