import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(width, height):
    """Create an empty board with specified width and height."""
    return [[" " for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board."""
    print("  A B C D E F G")
    for row in board:
        print("+---" * len(row) + "+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
    print("+---" * len(row) + "+")

def validate_input(input_str, board):
    """Check if the input is valid."""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    column = ord(input_str.upper()) - ord('A')
    if column < 0 or column >= len(board[0]):
        return False
    return True

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all([all([cell!= " " for cell in row]) for row in board])

def game():
    """Start a new game."""
    os.system('clear')
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    num_players = 2  # Can be changed to any number between MIN_PLAYERS and MAX_PLAYERS
    players = PLAYERS_CHECKERS[:num_players]
    current_player = random.choice(players)
    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        input_str = input().upper()
        if not validate_input(input_str, board):
            print("Invalid input. Please try again.")
            continue
        column = ord(input_str) - ord('A')
        drop_checker(board, column, current_player)
        os.system('clear')
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % num_players]

game()
