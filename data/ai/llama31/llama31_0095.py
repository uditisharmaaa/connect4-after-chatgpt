import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a new 2D board with all elements initialized to whitespace."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  A', end='')
    for col in range(1, BOARD_COLS):
        print('  ', chr(ord('A') + col), end='')
    print('\n+' + '+---' * BOARD_COLS + '+')
    for row in range(BOARD_ROWS):
        print('|   |' * BOARD_COLS + '|')
        print('|', end='')
        for col in range(BOARD_COLS):
            print(' ' + board[row][col] + ' |', end='')
        print('\n+' + '+---' * BOARD_COLS + '+')

def get_next_player(current_player):
    """Return the next player in the list of players."""
    return CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]

def is_valid_input(input_str):
    """Check if the user input is a valid column letter."""
    return input_str.upper() in 'ABCDEFG'

def get_input(player):
    """Get a valid input from the user."""
    while True:
        input_str = input(f"Player {player}, please enter a column: ")
        if is_valid_input(input_str):
            return input_str.upper()
        print("Invalid input. Please enter a letter between A and G.")

def drop_checker(board, col, player):
    """Drop a checker into the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][ord(col) - ord('A')] == ' ':
            board[row][ord(col) - ord('A')] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical locations for win
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

def check_draw(board):
    """Check if the board is full."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    os.system('clear')
    board = create_board()
    current_player = CHECKERS[random.randint(0, NUM_PLAYERS - 1)]
    while True:
        print_board(board)
        col = get_input(current_player)
        if not drop_checker(board, col, current_player):
            print("Column is full. Try again.")
            continue
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
