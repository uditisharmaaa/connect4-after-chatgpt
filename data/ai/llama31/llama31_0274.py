import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with whitespaces"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_num):
    """Get the checker symbol for a given player number"""
    return CHECKERS[player_num - 1]

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return input_str.upper() in 'ABCDEFG'

def get_column_index(input_str):
    """Get the column index from a valid input letter"""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, col_idx):
    """Check if a column is full"""
    return board[NUM_ROWS - 1][col_idx]!= ' '

def place_checker(board, player_num, col_idx):
    """Place a checker in a column"""
    for row_idx in range(NUM_ROWS):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = get_player_checker(player_num)
            return

def check_win(board, player_num):
    """Check if a player has won"""
    checker = get_player_checker(player_num)
    # Check horizontal
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS - 3):
            if board[row_idx][col_idx] == checker and \
               board[row_idx][col_idx + 1] == checker and \
               board[row_idx][col_idx + 2] == checker and \
               board[row_idx][col_idx + 3] == checker:
                return True
    # Check vertical
    for row_idx in range(NUM_ROWS - 3):
        for col_idx in range(NUM_COLS):
            if board[row_idx][col_idx] == checker and \
               board[row_idx + 1][col_idx] == checker and \
               board[row_idx + 2][col_idx] == checker and \
               board[row_idx + 3][col_idx] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row_idx in range(NUM_ROWS - 3):
        for col_idx in range(NUM_COLS - 3):
            if board[row_idx][col_idx] == checker and \
               board[row_idx + 1][col_idx + 1] == checker and \
               board[row_idx + 2][col_idx + 2] == checker and \
               board[row_idx + 3][col_idx + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row_idx in range(3, NUM_ROWS):
        for col_idx in range(NUM_COLS - 3):
            if board[row_idx][col_idx] == checker and \
               board[row_idx - 1][col_idx + 1] == checker and \
               board[row_idx - 2][col_idx + 2] == checker and \
               board[row_idx - 3][col_idx + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(board[NUM_ROWS - 1][col_idx]!= ' ' for col_idx in range(NUM_COLS))

def game():
    """Main game loop"""
    board = create_board()
    player_num = random.randint(1, NUM_PLAYERS)
    while True:
        os.system('clear')
        print_board(board)
        print('Player {}, please enter a column:'.format(get_player_checker(player_num)))
        input_str = input()
        if not is_valid_input(input_str):
            print('Invalid input. Please try again.')
            continue
        col_idx = get_column_index(input_str)
        if is_column_full(board, col_idx):
            print('Column is full. Please try again.')
            continue
        place_checker(board, player_num, col_idx)
        if check_win(board, player_num):
            os.system('clear')
            print_board(board)
            print('Player {} won!'.format(get_player_checker(player_num)))
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print('Game is a draw.')
            break
        player_num = (player_num % NUM_PLAYERS) + 1

if __name__ == '__main__':
    game()
