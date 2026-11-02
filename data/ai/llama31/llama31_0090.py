import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create an empty board with the given width and height."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * len(row))
        print('|   ' * len(row))
        print('| ' + ' | '.join(row))
        print('|   ' * len(row))
    print('+---' * len(board[0]))

def is_valid_input(column, width):
    """Check if the input is a valid column letter."""
    return 'A' <= column <= chr(ord('A') + width - 1)

def get_column_index(column):
    """Convert the column letter to a column index."""
    return ord(column) - ord('A')

def drop_checker(board, column, checker):
    """Drop the checker into the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_player = players[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ").upper()

        if not is_valid_input(column, BOARD_WIDTH):
            print("Invalid input. Please try again.")
            continue

        column_index = get_column_index(column)
        drop_checker(board, column_index, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
