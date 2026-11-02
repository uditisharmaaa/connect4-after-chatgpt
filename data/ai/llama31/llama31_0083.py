import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board"""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the game board"""
    os.system('clear')
    print('  A', ' B', ' C', ' D', ' E', ' F', ' G')
    for i in range(NUM_ROWS):
        print('+---' * NUM_COLS + '+')
        row = '| '
        for j in range(NUM_COLS):
            row += board[i][j] + ' | '
        print(row)
    print('+---' * NUM_COLS + '+')

def get_player_checker(player_num):
    """Get the checker for a given player"""
    return CHECKERS[player_num]

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return input_str.upper() in 'ABCDEFG'

def get_column(input_str):
    """Convert the input string to a column index"""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, col):
    """Check if a column is full"""
    return board[0][col]!= ' '

def drop_checker(board, col, checker):
    """Drop a checker into a column"""
    for i in range(NUM_ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = checker
            break

def check_win(board, player_checker):
    """Check for a win"""
    # Check horizontal
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS - 3):
            if board[i][j] == player_checker and board[i][j + 1] == player_checker and board[i][j + 2] == player_checker and board[i][j + 3] == player_checker:
                return True

    # Check vertical
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS):
            if board[i][j] == player_checker and board[i + 1][j] == player_checker and board[i + 2][j] == player_checker and board[i + 3][j] == player_checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS - 3):
            if board[i][j] == player_checker and board[i + 1][j + 1] == player_checker and board[i + 2][j + 2] == player_checker and board[i + 3][j + 3] == player_checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for i in range(3, NUM_ROWS):
        for j in range(NUM_COLS - 3):
            if board[i][j] == player_checker and board[i - 1][j + 1] == player_checker and board[i - 2][j + 2] == player_checker and board[i - 3][j + 3] == player_checker:
                return True

    return False

def is_draw(board):
    """Check if the game is a draw"""
    for i in range(NUM_COLS):
        if board[0][i] == ' ':
            return False
    return True

def game():
    board = create_board()
    players = [get_player_checker(i) for i in range(NUM_PLAYERS)]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")
        input_str = input().strip()
        if not is_valid_input(input_str):
            print("Invalid input. Please enter a letter between A and G.")
            continue
        col = get_column(input_str)
        if is_column_full(board, col):
            print("Column is full. Please choose another column.")
            continue
        drop_checker(board, col, players[current_player])
        if check_win(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

game()
