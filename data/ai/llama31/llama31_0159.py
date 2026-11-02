import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

# Create the board
def create_board():
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| {} |'.format(' | '.join(row)))
    print('+---' * BOARD_COLS + '+')
    print('  A B C D E F G')

# Validate user input
def validate_input(col):
    if col < 'A' or col > chr(64 + BOARD_COLS):
        return False
    return True

# Get the next available row in a column
def get_next_row(board, col):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][ord(col) - 65] == ' ':
            return row
    return -1

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True
    return False

# Game loop
def game_loop():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    print('Player {} will start.'.format(current_player))
    while True:
        print_board(board)
        col = input('Player {}, please enter a column: '.format(current_player))
        if not validate_input(col):
            print('Invalid input. Please enter a letter between A and G.')
            continue
        row = get_next_row(board, col)
        if row == -1:
            print('Column is full. Please choose another column.')
            continue
        board[row][ord(col) - 65] = current_player
        if check_win(board, current_player):
            print_board(board)
            print('Player {} won!'.format(current_player))
            break
        # Check for draw
        if all(all(cell!= ' ' for cell in row) for row in board):
            print_board(board)
            print('It\'s a draw!')
            break
        # Switch player
        current_player = players[(players.index(current_player) + 1) % len(players)]

game_loop()
