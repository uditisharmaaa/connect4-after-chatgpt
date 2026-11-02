import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a 2D board with the given dimensions."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the board in a human-readable format."""
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_WIDTH + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_WIDTH + '+')

def validate_input(input_str):
    """Validate the user's input."""
    if len(input_str)!= 1:
        return False
    if not input_str.isalpha():
        return False
    if not 'A' <= input_str.upper() <= 'G':
        return False
    return True

def get_column_index(input_str):
    """Convert the user's input to a column index."""
    return ord(input_str.upper()) - ord('A')

def drop_checker(board, column, checker):
    """Drop a checker into the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all(board[row][col] == checker for row in range(i, i+4)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(all(cell!= ' ' for cell in row) for row in board)

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = ['X', 'O']
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")

        input_str = input().strip()
        if not validate_input(input_str):
            print("Invalid input. Please try again.")
            continue

        column = get_column_index(input_str)
        if all(cell!= ' ' for cell in [row[column] for row in board]):
            print("Column is full. Please try again.")
            continue

        drop_checker(board, column, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()
