import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    """Create a 2D board with the given dimensions."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    print('  ' + ' '.join(chr(65+i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print('+---' * COLUMNS + '+')

def get_valid_columns(board):
    """Return a list of valid columns for the current player."""
    return [i for i in range(COLUMNS) if ' ' in board[:, i]]

def get_next_player(players, current_player):
    """Return the next player."""
    return players[(players.index(current_player) + 1) % len(players)]

def place_checker(board, column, checker):
    """Place a checker in the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the given player has won."""
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for i in range(ROWS - 3):
            if all(board[row][col] == checker for row in range(i, i+4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def game():
    # Create the board
    board = create_board(ROWS, COLUMNS)

    # Choose the first player
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    # Game loop
    while True:
        # Clear the screen and print the board
        os.system('clear')
        print_board(board)

        # Get the current player's move
        while True:
            move = input(f"Player {current_player}, please enter a column: ")
            if move.upper() in 'ABCDEFG':
                column = ord(move.upper()) - 65
                if column in get_valid_columns(board):
                    break
            print("Invalid move, please try again.")

        # Place the checker
        place_checker(board, column, current_player)

        # Check for a win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            return

        # Check for a draw
        if all(cell!= ' ' for row in board for cell in row):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            return

        # Switch to the next player
        current_player = get_next_player(players, current_player)

if __name__ == "__main__":
    game()
