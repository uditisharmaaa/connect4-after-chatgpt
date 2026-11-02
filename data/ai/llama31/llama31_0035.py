import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|   ' * NUM_COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * NUM_COLS + '+')

def get_player_checker(player_index):
    """Get the checker symbol for the given player index"""
    return CHECKERS[player_index]

def get_column_index(column):
    """Get the column index from the user input (A-G)"""
    return ord(column.upper()) - ord('A')

def is_valid_input(column):
    """Check if the user input is valid (A-G)"""
    return 'A' <= column.upper() <= 'G'

def is_column_full(board, column_index):
    """Check if the column is full"""
    return board[0][column_index]!= ' '

def drop_checker(board, column_index, checker):
    """Drop the checker into the column"""
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return

def check_win(board, checker):
    """Check for a win (horizontally, vertically, diagonally)"""
    # Check horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True

    # Check vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if all(board[row][col] == checker for row in range(i, i+4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player_index = 0

    while True:
        print_board(board)
        print(f"Player {get_player_checker(current_player_index)}, please enter a column:")
        column = input().strip()

        if not is_valid_input(column):
            print("Invalid input. Please try again.")
            continue

        column_index = get_column_index(column)
        if is_column_full(board, column_index):
            print("Column is full. Please try again.")
            continue

        checker = get_player_checker(current_player_index)
        drop_checker(board, column_index, checker)

        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
