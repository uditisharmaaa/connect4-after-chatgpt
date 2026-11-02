import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
MAX_PLAYERS = len(CHECKERS)

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels"""
    print('  ' + ' '.join(string.ascii_uppercase[:COLS]))
    print('+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLS + '+')

def validate_input(column, board):
    """Validate the user input"""
    if not column.isalpha():
        return False
    if column.upper() not in string.ascii_uppercase[:COLS]:
        return False
    if board[0][string.ascii_uppercase[:COLS].index(column.upper())]!= ' ':
        return False
    return True

def drop_checker(column, board, checker):
    """Drop the checker into the column"""
    for row in reversed(board):
        if row[string.ascii_uppercase[:COLS].index(column.upper())] == ' ':
            row[string.ascii_uppercase[:COLS].index(column.upper())] = checker
            return

def check_win(board, checker):
    """Check for a win"""
    # Horizontal
    for row in board:
        for i in range(COLS - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True
    # Vertical
    for col in range(COLS):
        for i in range(ROWS - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

def check_draw(board):
    """Check for a draw"""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the game"""
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()
        while not validate_input(column, board):
            print("Invalid input. Please enter a column:")
            column = input().upper()
        drop_checker(column, board, current_player)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

game()
