import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board(rows, columns):
    """Create a board initialized with whitespaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Clear screen and print the board."""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_input(column):
    """Check if the input is valid."""
    return column.isalpha() and 'A' <= column.upper() < chr(65 + COLUMNS)

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the current player has won."""
    # Check horizontal, vertical and diagonal lines
    for r in range(ROWS):
        for c in range(COLUMNS):
            # Horizontal
            if c <= COLUMNS - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical
            if r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal /
            if r <= ROWS - 4 and c <= COLUMNS - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Diagonal \
            if r <= ROWS - 4 and c >= 3 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check for a draw condition."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(CHECKERS)
    print_board(board)

    while True:
        print(f'Player {current_player}, please enter a column:')
        column = input().strip()

        # Validate input
        while not is_valid_input(column):
            print('Invalid input. Please enter a valid column letter:')
            column = input().strip()

        # Place checker and check for valid move
        if place_checker(board, column, current_player):
            print_board(board)

            # Check for win
            if check_winner(board, current_player):
                print(f'Player {current_player} won!')
                break

            # Check for draw
            if is_draw(board):
                print('The game is a draw!')
                break

            # Switch player
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
        else:
            print(f'Column {column} is full. Player {current_player} lost the turn.')

if __name__ == '__main__':
    main()
