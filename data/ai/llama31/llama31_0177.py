import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_CHECKERS_TO_WIN = 4

def create_board():
    """Create a 2D board with all elements initialized to whitespace."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players):
    """Print the current state of the board."""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---' * BOARD_COLS + '+')
    print(f'Player {players[0]}, please enter a column:')

def get_player_checker(players, player_index):
    """Get the checker of the current player."""
    return CHECKERS[player_index % len(players)]

def get_valid_move(board, column):
    """Get the index of the lowest available space in the column."""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][column] == ' ':
            return row_index
    return None

def make_move(board, column, checker):
    """Place a checker at the specified column."""
    row_index = get_valid_move(board, column)
    if row_index is not None:
        board[row_index][column] = checker
    else:
        raise ValueError('Column is full')

def check_win(board, checker):
    """Check if there are four checkers in a row."""
    # Check horizontal
    for row in board:
        for col in range(BOARD_COLS - NUM_CHECKERS_TO_WIN + 1):
            if all(row[col + i] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True
    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - NUM_CHECKERS_TO_WIN + 1):
            if all(board[row + i][col] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - NUM_CHECKERS_TO_WIN + 1):
        for col in range(BOARD_COLS - NUM_CHECKERS_TO_WIN + 1):
            if all(board[row + i][col + i] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(NUM_CHECKERS_TO_WIN - 1, BOARD_ROWS):
        for col in range(BOARD_COLS - NUM_CHECKERS_TO_WIN + 1):
            if all(board[row - i][col + i] == checker for i in range(NUM_CHECKERS_TO_WIN)):
                return True
    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    num_players = 2
    players = list(range(num_players))
    board = create_board()
    current_player_index = random.randint(0, num_players - 1)
    while True:
        os.system('clear')
        print_board(board, players)
        column = input().upper()
        if not column.isalpha() or not 'A' <= column <= 'G':
            print('Invalid input. Please enter a letter between A and G.')
            continue
        column = ord(column) - ord('A')
        try:
            make_move(board, column, get_player_checker(players, current_player_index))
        except ValueError:
            print('Column is full. Please choose another column.')
            continue
        if check_win(board, get_player_checker(players, current_player_index)):
            os.system('clear')
            print_board(board, players)
            print(f'Player {get_player_checker(players, current_player_index)} won!')
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board, players)
            print('It\'s a draw!')
            break
        current_player_index = (current_player_index + 1) % num_players

game()
