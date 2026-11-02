import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(BOARD_COLS)))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')

def get_player_checker(player):
    """Return the checker symbol for the given player."""
    return CHECKERS[player - 1]

def is_valid_input(input_str):
    """Check if the input is a valid column letter."""
    return input_str.isalpha() and len(input_str) == 1 and 65 <= ord(input_str) <= 65 + BOARD_COLS - 1

def get_column(input_str):
    """Convert the input string to a column index."""
    return ord(input_str) - 65

def is_column_full(board, column):
    """Check if the given column is full."""
    return board[0][column]!= ' '

def drop_checker(board, column, checker):
    """Drop the checker into the given column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return

def check_win(board, checker):
    """Check if the given player has won."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(all(cell!= ' ' for cell in row) for row in board)

def main():
    board = create_board()
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board)
        player = players[current_player]
        checker = get_player_checker(player)
        print(f'Player {checker}, please enter a column: ')

        while True:
            input_str = input().upper()
            if is_valid_input(input_str):
                column = get_column(input_str)
                if not is_column_full(board, column):
                    drop_checker(board, column, checker)
                    break
                else:
                    print('Column is full. Please choose another column.')
            else:
                print('Invalid input. Please enter a column letter.')

        if check_win(board, checker):
            print_board(board)
            print(f'Player {checker} won!')
            break
        elif check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
