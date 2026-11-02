import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board, columns):
    labels = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(labels))
    for row in board:
        print("+---" * columns + "+")
        print("|   " * columns + "|")
        print("|   ".join(row) + " |")
        print("|   " * columns + "|")
    print("+---" * columns + "+")

# Function to validate user input
def validate_input(user_input, columns):
    if len(user_input)!= 1 or not user_input.isalpha():
        return False
    if ord(user_input.upper()) - ord('A') < 0 or ord(user_input.upper()) - ord('A') >= columns:
        return False
    return True

# Function to check for win
def check_win(board, checker, rows, columns):
    # Check horizontal
    for row in board:
        for i in range(columns - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical
    for col in range(columns):
        for i in range(rows - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True

    # Check positive diagonal
    for row in range(rows - 3):
        for col in range(columns - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negative diagonal
    for row in range(3, rows):
        for col in range(columns - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

# Function to check for draw
def check_draw(board):
    return all(all(cell!= " " for cell in row) for row in board)

# Main game loop
def play_game():
    os.system('clear')
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board, BOARD_COLUMNS)
    while True:
        current_player = players[current_player_index]
        print("Player", current_player, "please enter a column:")
        user_input = input().upper()
        while not validate_input(user_input, BOARD_COLUMNS):
            print("Invalid input. Please try again.")
            user_input = input().upper()
        column_index = ord(user_input) - ord('A')
        for i in range(BOARD_ROWS - 1, -1, -1):
            if board[i][column_index] == " ":
                board[i][column_index] = current_player
                break
        else:
            print("Column is full. Please try again.")
            continue
        os.system('clear')
        print_board(board, BOARD_COLUMNS)
        if check_win(board, current_player, BOARD_ROWS, BOARD_COLUMNS):
            print("Player", current_player, "won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
