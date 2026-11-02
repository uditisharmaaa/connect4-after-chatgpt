import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with given dimensions."""
    return [[' ']*BOARD_COLS for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def get_valid_input():
    """Get a valid column input from the user."""
    while True:
        col = input("Enter a column (A-{}): ".format(string.ascii_uppercase[BOARD_COLS-1]))
        if col.upper() in string.ascii_uppercase[:BOARD_COLS]:
            return col.upper()

def place_checker(board, col, checker):
    """Place a checker at the given column."""
    col_idx = ord(col) - ord('A')
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return

def check_win(board, checker):
    """Check for a win condition."""
    # Horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True
    # Vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True
    # Diagonal
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
            if board[row][col+3] == board[row+1][col+2] == board[row+2][col+1] == board[row+3][col] == checker:
                return True
    return False

def game():
    """Start the game."""
    num_players = 2
    players = CHECKERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)
    board = create_board()
    os.system('clear')
    print_board(board)

    while True:
        current_player = players[current_player_idx]
        print("Player {}, please enter a column:".format(current_player))
        col = get_valid_input()
        place_checker(board, col, current_player)
        os.system('clear')
        print_board(board)
        if check_win(board, current_player):
            print("Player {} won!".format(current_player))
            break
        if all(cell!= ' ' for row in board for cell in row):
            print("It's a draw!")
            break
        current_player_idx = (current_player_idx + 1) % num_players

game()
