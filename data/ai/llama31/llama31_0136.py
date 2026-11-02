import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates an empty board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players, current_player):
    """Prints the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')
    print(f'Player {current_player}, please enter a column:')

def is_valid_input(column):
    """Checks if the input is a valid column letter."""
    return 'A' <= column <= chr(65 + BOARD_COLS - 1)

def get_column_index(column):
    """Converts a column letter to a column index."""
    return ord(column) - 65

def is_valid_move(board, column_index):
    """Checks if the move is valid (i.e., the column is not full)."""
    return board[0][column_index] == ' '

def make_move(board, column_index, checker):
    """Makes a move by placing the checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = checker
            return

def check_win(board, checker):
    """Checks if the current player has won."""
    # Check horizontal wins
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True
    # Check vertical wins
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True
    # Check diagonal wins
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True
            if board[row][col + 3] == board[row + 1][col + 2] == board[row + 2][col + 1] == board[row + 3][col] == checker:
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    num_players = 2
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    board = create_board()
    while True:
        print_board(board, players, players[current_player_index])
        column = input().upper()
        while not is_valid_input(column) or not is_valid_move(board, get_column_index(column)):
            print("Invalid input. Please enter a column letter.")
            column = input().upper()
        make_move(board, get_column_index(column), players[current_player_index])
        if check_win(board, players[current_player_index]):
            print_board(board, players, players[current_player_index])
            print(f"Player {players[current_player_index]} won!")
            break
        elif check_draw(board):
            print_board(board, players, players[current_player_index])
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % num_players

game()
