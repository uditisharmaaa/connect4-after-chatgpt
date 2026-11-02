import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players, current_player):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(BOARD_COLS)))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')
    print(f"Player {CHECKERS[current_player - 1]}, please enter a column: ")

def validate_input(col):
    """Validate the user's input."""
    if not col.isalpha():
        return False
    col = ord(col.upper()) - 65
    return 0 <= col < BOARD_COLS

def place_checker(board, col, player):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = CHECKERS[player - 1]
            return True
    return False

def check_win(board, player):
    """Check for a win in the current board state."""
    checker = CHECKERS[player - 1]
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i + 4]]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == checker for row in range(i, i + 4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row + i][col + i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row - i][col + i] == checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check if the board is full."""
    return all([cell!= ' ' for row in board for cell in row])

def game():
    """The main game loop."""
    board = create_board()
    players = 2
    current_player = random.randint(1, players)
    while True:
        print_board(board, players, current_player)
        col = input().upper()
        while not validate_input(col):
            print("Invalid input. Please enter a letter.")
            col = input().upper()
        col = ord(col) - 65
        if not place_checker(board, col, current_player):
            print("Column is full. Please choose another column.")
            continue
        if check_win(board, current_player):
            print_board(board, players, current_player)
            print(f"Player {CHECKERS[current_player - 1]} won!")
            break
        if check_draw(board):
            print_board(board, players, current_player)
            print("It's a draw!")
            break
        current_player = (current_player % players) + 1

if __name__ == "__main__":
    game()
