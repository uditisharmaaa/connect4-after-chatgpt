import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a 2D list representing the game board."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the game board."""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * BOARD_WIDTH + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_WIDTH + '+')

def validate_input(column):
    """Validate user input."""
    if len(column)!= 1:
        return False
    if column not in string.ascii_uppercase[:BOARD_WIDTH]:
        return False
    return True

def get_next_player(current_player):
    """Get the next player."""
    return (current_player + 1) % NUM_PLAYERS

def place_checker(board, column, checker):
    """Place a checker on the board."""
    column_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if a player has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True

    # Check diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
            if board[row][col+3] == checker and board[row+1][col+2] == checker and board[row+2][col+1] == checker and board[row+3][col] == checker:
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
    # Create the game board
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)

    # Choose a random first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Main game loop
    while True:
        # Clear the screen
        os.system('clear')

        # Print the game board
        print_board(board)

        # Get user input
        while True:
            column = input(f"Player {CHECKERS[current_player]}, please enter a column: ")
            if validate_input(column):
                break
            print("Invalid input. Please try again.")

        # Place the checker
        if not place_checker(board, column, CHECKERS[current_player]):
            print("Column is full. Try again.")
            continue

        # Check if the game is won or drawn
        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
