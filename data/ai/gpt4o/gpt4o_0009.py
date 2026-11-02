import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(i + ord('A')) for i in range(COLUMNS))
    print(header)
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def get_player_input():
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if column.isalpha() and 'A' <= column <= chr(ord('A') + COLUMNS - 1):
            return ord(column) - ord('A')
        print("Invalid input. Please enter a valid column.")

def drop_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def play_game():
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        column = get_player_input()
        if drop_checker(board, column, CHECKERS[current_player_idx]):
            if check_win(board, CHECKERS[current_player_idx]):
                print_board(board)
                print(f"Player {CHECKERS[current_player_idx]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            print("Column is full. Turn lost.")

# Start the game
play_game()
