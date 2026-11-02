import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
MAX_PLAYERS = 5
MAX_COLUMNS = 26
COLUMN_LABELS = [chr(c) for c in range(ord('A'), ord('A') + COLUMNS)]

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def get_valid_input(board):
    """Get a valid column choice from the current player."""
    while True:
        choice = input('Please enter a column: ').upper()
        if choice not in COLUMN_LABELS:
            print(f"Invalid input! Choose between {', '.join(COLUMN_LABELS)}.")
        else:
            column_index = COLUMN_LABELS.index(choice)
            if board[0][column_index] != ' ':
                print("Column is full! Choose another one.")
            else:
                return column_index

def place_checker(board, column, checker):
    """Place the current player's checker in the chosen column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def has_won(board, checker):
    """Check if the current player has won."""
    # Horizontal Check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True
    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal Check (Descending)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal Check (Ascending)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Run the Connect 4 game loop."""
    board = initialize_board()
    players = CHECKERS[:PLAYERS]
    random.shuffle(players)
    current_player_index = 0

    print_board(board)
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}'s turn.")
        column = get_valid_input(board)
        place_checker(board, column, current_checker)
        
        print_board(board)

        if has_won(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif is_draw(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

play_game()
