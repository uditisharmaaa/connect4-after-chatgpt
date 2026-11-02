import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def initialize_board():
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# Print the board
def print_board(board, current_player):
    print('  A B C D E F G')
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            print('| ' + board[row][col], end='')
        print('|')
        print('+---+---+---+---+---+---+---+')
    print('Player ' + CHECKERS[current_player] + ', please enter a column:')

# Get the column index from the user's input
def get_column_index(col):
    return ord(col.upper()) - ord('A')

# Check if the user's input is valid
def is_valid_input(col, board):
    try:
        col_index = get_column_index(col)
        if col_index < 0 or col_index >= BOARD_COLS:
            return False
        if board[0][col_index]!= ' ':
            return False
        return True
    except ValueError:
        return False

# Place the checker at the correct location
def place_checker(board, col, player):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = CHECKERS[player]
            return

# Check for a win
def check_win(board, player):
    checker = CHECKERS[player]
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

# Check for a draw
def check_draw(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

# Main game loop
def game_loop():
    board = initialize_board()
    num_players = 2
    current_player = random.randint(0, num_players - 1)
    while True:
        os.system('clear')
        print_board(board, current_player)
        col = input().strip()
        if not is_valid_input(col, board):
            print('Invalid input. Please try again.')
            continue
        col_index = get_column_index(col)
        place_checker(board, col_index, current_player)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board, current_player)
            print('Player ' + CHECKERS[current_player] + ' won!')
            break
        if check_draw(board):
            os.system('clear')
            print_board(board, current_player)
            print('It\'s a draw!')
            break
        current_player = (current_player + 1) % num_players

game_loop()
