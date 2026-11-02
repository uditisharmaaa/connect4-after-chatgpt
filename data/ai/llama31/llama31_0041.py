import os
import random

# Global constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespace."""
    board = []
    for _ in range(NUM_ROWS):
        row = [' ' for _ in range(NUM_COLS)]
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    print('  A B C D E F G')
    for i, row in enumerate(board, start=1):
        print('+---' * NUM_COLS + '+')
        print('|', end='')
        for cell in row:
            print(' {} |'.format(cell), end='')
        print()
    print('+---' * NUM_COLS + '+')

def get_valid_input(player, board):
    """Get a valid column input from the user."""
    while True:
        col = input('Player {}, please enter a column: '.format(player)).upper()
        if col not in 'ABCDEFG':
            print('Invalid column. Please enter a letter between A and G.')
        else:
            col_index = ord(col) - ord('A')
            if board[NUM_ROWS - 1][col_index]!= ' ':
                print('Column is full. Please choose another column.')
            else:
                return col_index

def place_checker(board, col, player):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_win(board, player):
    """Check if the specified player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == player:
                return True

    # Check vertical wins
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the game."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    os.system('clear')
    print_board(board)

    while True:
        col = get_valid_input(current_player, board)
        place_checker(board, col, current_player)

        os.system('clear')
        print_board(board)

        if check_win(board, current_player):
            print('Player {} won!'.format(current_player))
            break

        if check_draw(board):
            print('It\'s a draw!')
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

game()
