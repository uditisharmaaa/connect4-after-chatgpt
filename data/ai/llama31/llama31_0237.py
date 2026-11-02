import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  ' + ' '.join(chr(65+i) for i in range(BOARD_COLS)))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')

def is_valid_move(board, col):
    """Check if a move is valid (i.e., the column is not full)."""
    return board[0][col] == ' '

def make_move(board, col, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    """Check if a player has won."""
    # Check horizontal
    for row in board:
        for i in range(BOARD_COLS - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if all(board[row][col] == checker for row in range(i, i+4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the Connect 4 game."""
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{chr(64+BOARD_COLS)}):")

        while True:
            move = input().upper()
            if move < 'A' or move > chr(64+BOARD_COLS):
                print("Invalid input. Please enter a column letter.")
            elif not is_valid_move(board, ord(move) - 65):
                print("Column is full. Please choose another column.")
            else:
                make_move(board, ord(move) - 65, current_player)
                break

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

game()
