import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D list representing the game board"""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board"""
    os.system('clear')
    print('  A', 'B', 'C', 'D', 'E', 'F', 'G', sep='  ')
    for i, row in enumerate(board):
        print('+---' * COLUMNS + '+')
        print('|', end='')
        for j, cell in enumerate(row):
            print(' {} |'.format(cell), end='')
        print()
    print('+---' * COLUMNS + '+')

def get_player_checker(player_index):
    """Get the checker for the given player"""
    return CHECKERS[player_index]

def is_valid_column(column):
    """Check if the given column is valid"""
    return 'A' <= column <= chr(ord('A') + COLUMNS - 1)

def is_valid_move(board, column):
    """Check if the given move is valid"""
    column_index = ord(column) - ord('A')
    return board[0][column_index] == ' '

def get_next_open_row(board, column):
    """Get the next open row in the given column"""
    column_index = ord(column) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == ' ':
            return row
    return -1

def drop_checker(board, player_checker, column):
    """Drop the checker in the given column"""
    row = get_next_open_row(board, column)
    if row!= -1:
        board[row][ord(column) - ord('A')] = player_checker

def check_win(board, player_checker):
    """Check if the given player has won"""
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player_checker and
                board[row][col + 1] == player_checker and
                board[row][col + 2] == player_checker and
                board[row][col + 3] == player_checker):
                return True

    # Check vertical wins
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (board[row][col] == player_checker and
                board[row + 1][col] == player_checker and
                board[row + 2][col] == player_checker and
                board[row + 3][col] == player_checker):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player_checker and
                board[row + 1][col + 1] == player_checker and
                board[row + 2][col + 2] == player_checker and
                board[row + 3][col + 3] == player_checker):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player_checker and
                board[row - 1][col + 1] == player_checker and
                board[row - 2][col + 2] == player_checker and
                board[row - 3][col + 3] == player_checker):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == ' ':
                return False
    return True

def play_game():
    """Play the Connect 4 game"""
    board = create_board()
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = players.pop(0)

    while True:
        print_board(board)
        print("Player", get_player_checker(current_player), ", please enter a column:")
        column = input().upper()
        while not is_valid_column(column) or not is_valid_move(board, column):
            print("Invalid move, try again:")
            column = input().upper()
        drop_checker(board, get_player_checker(current_player), column)
        if check_win(board, get_player_checker(current_player)):
            print_board(board)
            print("Player", get_player_checker(current_player), "won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players.pop(0) if players else players.append(current_player) and players[0]

play_game()
