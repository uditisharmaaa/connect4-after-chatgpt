import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    print('+' + '+'.join(['---' for _ in range(BOARD_COLS)]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '+'.join(['---' for _ in range(BOARD_COLS)]) + '+')

def get_player_checker(player):
    """Get the checker for the given player."""
    return CHECKERS[player]

def is_valid_input(input_str):
    """Check if the input is a valid column letter."""
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str.upper() <= 'G'

def get_column_index(input_str):
    """Get the column index from the input string."""
    return string.ascii_uppercase.index(input_str.upper())

def is_valid_column(board, col):
    """Check if the column is not full."""
    return board[0][col] == ' '

def drop_checker(board, col, checker):
    """Drop the checker into the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return

def check_win(board, checker):
    """Check for a win."""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check for a draw."""
    return all([all([cell!= ' ' for cell in row]) for row in board])

def game():
    """Play the Connect 4 game."""
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {get_player_checker(players[current_player])}, please enter a column:")

        input_str = input().upper()
        while not is_valid_input(input_str):
            print("Invalid input. Please enter a column letter.")
            input_str = input().upper()

        col = get_column_index(input_str)
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue

        drop_checker(board, col, get_player_checker(players[current_player]))

        if check_win(board, get_player_checker(players[current_player])):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(players[current_player])} won!")
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

game()
