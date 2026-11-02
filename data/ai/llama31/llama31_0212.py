import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the specified dimensions"""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A', end='')
    for col in range(1, BOARD_COLS):
        print(' ' + chr(ord('A') + col), end='')
    print('\n+---' * BOARD_COLS + '+')
    for row in range(BOARD_ROWS):
        print('|', end='')
        for col in range(BOARD_COLS):
            print(' ' + board[row][col] + ' |', end='')
        print('\n+---' * BOARD_COLS + '+')

def validate_input(input_str):
    """Validate the user's input"""
    if len(input_str)!= 1 or input_str not in string.ascii_uppercase:
        return False
    col = ord(input_str) - ord('A')
    if col < 0 or col >= BOARD_COLS:
        return False
    return True

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won"""
    # Check horizontal wins
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical wins
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def game():
    """Main game loop"""
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print('Player', current_player, 'please enter a column:')
        input_str = input().upper()
        while not validate_input(input_str):
            print('Invalid input. Please try again:')
            input_str = input().upper()
        col = ord(input_str) - ord('A')
        if not place_checker(board, col, current_player):
            print('Column is full. Please try again:')
            continue
        if check_win(board, current_player):
            print_board(board)
            print('Player', current_player, 'won!')
            break
        if check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

game()
