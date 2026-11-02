import os
import random

# Constant global variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Create a 2D board with whitespaces.
    """
    board = [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """
    Print the board with columns labeled by letters.
    """
    print('  A', end='')
    for i in range(1, BOARD_COLUMNS):
        print(f' {chr(65 + i)}', end='')
    print()
    print('+---' * BOARD_COLUMNS + '+')
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        print('+---' * BOARD_COLUMNS + '+')

def get_player_checker(num_players):
    """
    Get the checker for the current player.
    """
    return CHECKERS[num_players % len(CHECKERS)]

def is_valid_input(input_str):
    """
    Check if the input is a valid column label.
    """
    return input_str.isalpha() and input_str.upper() in 'ABCDEFG'

def get_column_index(input_str):
    """
    Convert the input column label to an index.
    """
    return ord(input_str.upper()) - 65

def is_valid_move(board, column_index):
    """
    Check if the move is valid (i.e., the column is not full).
    """
    return board[0][column_index] == ' '

def make_move(board, player_checker, column_index):
    """
    Place the checker in the column.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = player_checker
            break

def check_win(board, player_checker):
    """
    Check for a win (horizontally, vertically, or diagonally).
    """
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == player_checker for cell in row[i:i+4]]):
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == player_checker for row in range(i, i+4)]):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == player_checker for i in range(4)]):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == player_checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """
    Check if the board is full (i.e., a draw).
    """
    return all([all([cell!= ' ' for cell in row]) for row in board])

def game_loop():
    """
    The main game loop.
    """
    num_players = 2  # Set the number of players
    board = create_board()
    current_player = random.randint(0, num_players - 1)
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column:")
        input_str = input().strip()
        if not is_valid_input(input_str):
            print("Invalid input. Please try again.")
            continue
        column_index = get_column_index(input_str)
        if not is_valid_move(board, column_index):
            print("Column is full. Please try again.")
            continue
        make_move(board, get_player_checker(current_player), column_index)
        if check_win(board, get_player_checker(current_player)):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    game_loop()
