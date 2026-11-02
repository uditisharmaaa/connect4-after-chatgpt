import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a new Connect 4 board"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the Connect 4 board"""
    os.system('clear')
    print('  A', end='')
    for col in range(1, BOARD_COLS):
        print('   ', chr(ord('A') + col), end='')
    print('\n+' + '+---' * BOARD_COLS + '+')
    for row in range(BOARD_ROWS):
        print('|', end='')
        for col in range(BOARD_COLS):
            print('   ' + board[row][col] + ' |', end='')
        print('\n+' + '+---' * BOARD_COLS + '+')
    print()

def validate_input(input_str, board):
    """Validate user input"""
    if len(input_str)!= 1 or not input_str.isalpha() or ord(input_str) - ord('A') < 0 or ord(input_str) - ord('A') >= BOARD_COLS:
        return False
    col = ord(input_str) - ord('A')
    for row in range(BOARD_ROWS):
        if board[row][col] == ' ':
            return True
    return False

def place_checker(input_str, player, board):
    """Place a checker on the board"""
    col = ord(input_str) - ord('A')
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_win(board, player):
    """Check for a win"""
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
    # Check diagonal
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True
            if board[row][col + 3] == player and board[row + 1][col + 2] == player and board[row + 2][col + 1] == player and board[row + 3][col] == player:
                return True
    return False

def check_draw(board):
    """Check for a draw"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board)
        print('Player', current_player, ', please enter a column:')
        input_str = input().upper()
        while not validate_input(input_str, board):
            print('Invalid input, please try again:')
            input_str = input().upper()
        place_checker(input_str, current_player, board)
        if check_win(board, current_player):
            print_board(board)
            print('Player', current_player, 'won!')
            break
        if check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == '__main__':
    main()
