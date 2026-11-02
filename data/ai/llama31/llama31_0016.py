import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a new Connect 4 board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    print('  A', end='')
    for col in range(1, BOARD_COLS):
        print(' ', chr(ord('A') + col), end='')
    print()
    print('+---' * BOARD_COLS + '+')
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            print('|', board[row][col], end=' ')
        print('|')
        print('+---' * BOARD_COLS + '+')

def get_player_checker(player_index):
    """Get the checker for the given player."""
    return CHECKERS[player_index]

def is_valid_input(input_str):
    """Check if the user input is a valid column."""
    return len(input_str) == 1 and 'A' <= input_str.upper() <= chr(ord('A') + BOARD_COLS - 1)

def get_column_index(input_str):
    """Get the column index from the user input."""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, col_index):
    """Check if the given column is full."""
    return board[0][col_index]!= ' '

def place_checker(board, col_index, checker):
    """Place the checker in the given column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return

def check_win(board, checker):
    """Check if the given checker has won."""
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
    """Check if the game is a draw."""
    for col in range(BOARD_COLS):
        if not is_column_full(board, col):
            return False
    return True

def game():
    num_players = 2
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(0, num_players - 1)

    while True:
        os.system('clear')
        print_board(board)
        print('Player', get_player_checker(current_player), 'please enter a column:')
        input_str = input().strip()

        if not is_valid_input(input_str):
            print('Invalid input. Please try again.')
            continue

        col_index = get_column_index(input_str)

        if is_column_full(board, col_index):
            print('Column is full. Please try again.')
            continue

        place_checker(board, col_index, get_player_checker(current_player))

        if check_win(board, get_player_checker(current_player)):
            os.system('clear')
            print_board(board)
            print('Player', get_player_checker(current_player), 'won!')
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print('It\'s a draw!')
            break

        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    game()
