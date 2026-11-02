import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board():
    """Create an empty board with the given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  A   B   C   D   E   F   G')
    print('+---+---+---+---+---+---+---+')
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        print('+---+---+---+---+---+---+---+')

def validate_input(player, column):
    """Check if the user input is valid."""
    if not column.isalpha():
        return False
    if column.upper() < 'A' or column.upper() > 'G':
        return False
    if board[0][ord(column.upper()) - 65]!= ' ':
        return False
    return True

def drop_checker(board, player, column):
    """Drop the checker into the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][ord(column.upper()) - 65] == ' ':
            board[row][ord(column.upper()) - 65] = player
            return

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal wins
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical wins
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

board = create_board()
players = CHECKERS[:NUM_PLAYERS]
current_player_index = random.randint(0, NUM_PLAYERS - 1)

while True:
    os.system('clear')
    print_board(board)
    current_player = players[current_player_index]
    print(f"Player {current_player}, please enter a column:")
    column = input().upper()
    while not validate_input(current_player, column):
        print("Invalid input. Please try again.")
        column = input().upper()
    drop_checker(board, current_player, column)
    if check_win(board, current_player):
        os.system('clear')
        print_board(board)
        print(f"Player {current_player} won!")
        break
    if check_draw(board):
        os.system('clear')
        print_board(board)
        print("It's a draw!")
        break
    current_player_index = (current_player_index + 1) % NUM_PLAYERS
