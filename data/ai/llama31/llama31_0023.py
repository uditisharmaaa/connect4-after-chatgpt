import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with the given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    print('  ' + ' '.join(chr(65 + i) for i in range(COLS)))  # Print column labels
    print('  ' + '+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('  ' + '+---' * COLS + '+')

def validate_input(col, cols):
    """Validate the user's input."""
    try:
        col = ord(col.upper()) - 65  # Convert column label to index
        if col < 0 or col >= cols:
            return False
        return True
    except ValueError:
        return False

def drop_checker(board, col, checker):
    """Drop the checker into the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, rows, cols, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in board:
        for i in range(cols - 3):
            if all(row[i + j] == checker for j in range(4)):
                return True

    # Check vertical
    for col in range(cols):
        for i in range(rows - 3):
            if all(board[i + j][col] == checker for j in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + j][col + j] == checker for j in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - j][col + j] == checker for j in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the Connect 4 game."""
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    os.system('clear')
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        col = input()
        if not validate_input(col, COLS):
            print("Invalid input. Please try again.")
            continue

        col = ord(col.upper()) - 65  # Convert column label to index
        if all(board[row][col]!= ' ' for row in range(ROWS)):
            print("Column is full. Please try again.")
            continue

        drop_checker(board, col, current_player)

        os.system('clear')
        print_board(board)

        if check_win(board, ROWS, COLS, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    game()
