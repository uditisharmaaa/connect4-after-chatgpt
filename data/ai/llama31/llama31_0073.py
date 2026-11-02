import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(columns, rows):
    """Create a 2D board with specified columns and rows."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    """Print the current state of the board."""
    print('  ' + ' '.join(chr(65 + i) for i in range(columns)))  # Print column labels
    for row in board:
        print('+---' * columns + '+')
        print('|   ' * columns + '|')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * columns + '+')

def is_valid_input(column, columns):
    """Check if the input column is valid."""
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < columns

def place_checker(board, column, checker):
    """Place the checker at the specified column."""
    column = ord(column.upper()) - 65
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, columns, rows, checker):
    """Check if the specified checker has won."""
    # Check horizontal
    for row in board:
        for i in range(columns - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True

    # Check vertical
    for col in range(columns):
        for i in range(rows - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    os.system('clear')
    num_players = 2
    checkers = CHECKERS[:num_players]
    board = initialize_board(BOARD_COLUMNS, BOARD_ROWS)
    current_player = random.randint(0, num_players - 1)

    while True:
        print_board(board, BOARD_COLUMNS)
        column = input(f"Player {checkers[current_player]}, please enter a column: ")
        if not is_valid_input(column, BOARD_COLUMNS):
            print("Invalid input. Please try again.")
            continue
        place_checker(board, column, checkers[current_player])
        if check_win(board, BOARD_COLUMNS, BOARD_ROWS, checkers[current_player]):
            print_board(board, BOARD_COLUMNS)
            print(f"Player {checkers[current_player]} won!")
            break
        elif check_draw(board):
            print_board(board, BOARD_COLUMNS)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
