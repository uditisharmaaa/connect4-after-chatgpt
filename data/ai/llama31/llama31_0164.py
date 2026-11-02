import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  ' + ' '.join(chr(65+i) for i in range(BOARD_WIDTH)))
    for row in board:
        print('+---' * BOARD_WIDTH + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_WIDTH + '+')

def get_player_checker(player):
    """Get the checker symbol for a given player"""
    return CHECKERS[player-1]

def get_valid_columns(board):
    """Get the columns that are not full"""
    return [i for i in range(BOARD_WIDTH) if ' ' in [row[i] for row in board]]

def is_valid_input(input_str, valid_columns):
    """Check if the user input is valid"""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    column = ord(input_str.upper()) - 65
    return column in valid_columns

def place_checker(board, column, checker):
    """Place a checker in the lowest available space in a column"""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if a player has won"""
    # Check horizontal
    for row in board:
        for i in range(BOARD_WIDTH - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True
    return False

def play_game():
    """Play the Connect 4 game"""
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = players[0]

    while True:
        print_board(board)
        valid_columns = get_valid_columns(board)
        checker = get_player_checker(current_player)
        while True:
            input_str = input(f"Player {checker}, please enter a column: ")
            if is_valid_input(input_str, valid_columns):
                column = ord(input_str.upper()) - 65
                break
            print("Invalid input, please try again.")

        place_checker(board, column, checker)
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            return
        if all([all([cell!= ' ' for cell in row]) for row in board]):
            print_board(board)
            print("It's a draw!")
            return

        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

play_game()
