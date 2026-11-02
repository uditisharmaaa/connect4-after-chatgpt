import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')

def is_valid_input(col, board):
    if not col.isalpha():
        return False
    col = ord(col.upper()) - ord('A')
    if col < 0 or col >= BOARD_COLS:
        return False
    return board[0][col] == ' '

def is_win(board, player):
    # Check horizontal
    for row in board:
        for i in range(BOARD_COLS - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == player:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player:
                return True

    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def play_game():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board)
        print('Player', current_player, 'please enter a column:')
        col = input().upper()
        while not is_valid_input(col, board):
            print('Invalid input. Please try again.')
            col = input().upper()
        col = ord(col) - ord('A')
        for row in range(BOARD_ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = current_player
                break
        if is_win(board, current_player):
            print_board(board)
            print('Player', current_player, 'won!')
            break
        elif is_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

play_game()
