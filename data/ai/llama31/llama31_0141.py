import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespace elements"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board, players):
    """Print the current state of the board"""
    print('  A', ' B', ' C', ' D', ' E', ' F', ' G')
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|', end='')
        for cell in row:
            if cell == ' ':
                print('   |', end='')
            else:
                print(' ' + cell + ' |', end='')
        print()
    print('+---' * NUM_COLS + '+')
    print("Player " + players[0] + ", please enter a column:")

def validate_input(col, board):
    """Check if the input is valid"""
    if not col.isalpha():
        return False
    col = ord(col.upper()) - 65
    if col < 0 or col >= NUM_COLS:
        return False
    for row in reversed(board):
        if row[col] == ' ':
            return True
    return False

def drop_checker(board, col, player):
    """Drop the checker into the specified column"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True

    # Check vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    # Initialize game variables
    board = create_board()
    players = CHECKERS[:2]  # Use 2 players for now
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board, [current_player])

        # Get user input
        col = input().strip()

        # Validate input
        if not validate_input(col, board):
            continue

        # Drop the checker
        col = ord(col.upper()) - 65
        drop_checker(board, col, current_player)

        # Check for win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board, [current_player])
            print("Player " + current_player + " won!")
            break

        # Check for draw
        if check_draw(board):
            os.system('clear')
            print_board(board, [current_player])
            print("It's a draw!")
            break

        # Switch players
        current_player = players[0] if current_player == players[1] else players[1]

game()
