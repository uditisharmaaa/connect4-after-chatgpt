import os
import random

# Constant global variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board, current_player):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLUMNS)))
    print('+---' * BOARD_COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLUMNS + '+')
    print(f"Player {current_player}, please enter a column:")

def validate_input(column):
    """Validate user input."""
    if not column.isalpha() or len(column)!= 1 or ord(column) < 65 or ord(column) > 65 + BOARD_COLUMNS - 1:
        return False
    return True

def place_checker(board, column, player):
    """Place a checker in the specified column."""
    column = ord(column) - 65
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(BOARD_COLUMNS - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == player:
                return True

    # Check vertical wins
    for col in range(BOARD_COLUMNS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def game():
    """The main game loop."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board, current_player)
        column = input().upper()
        while not validate_input(column):
            print("Invalid input. Please try again.")
            column = input().upper()
        if place_checker(board, column, current_player):
            if check_win(board, current_player):
                print_board(board, current_player)
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print_board(board, current_player)
                print("It's a draw!")
                break
            current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]
        else:
            print("Column is full. Please try again.")

if __name__ == "__main__":
    game()
