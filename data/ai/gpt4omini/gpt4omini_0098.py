import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a game board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)

    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(column, board):
    """Check if the player's choice of column is valid."""
    if len(column) != 1 or not ('A' <= column <= chr(65 + COLUMNS - 1)):
        return False
    column_index = ord(column) - 65
    return board[0][column_index] == ' '  # Column must not be full

def drop_checker(board, column, checker):
    """Drop the checker's piece into the chosen column."""
    column_index = ord(column) - 65
    for row in reversed(range(ROWS)):
        if board[row][column_index] == ' ':
            board[row][column_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Check for a winning condition for the given checker."""
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_horizontal(board, row, col, checker) or
                check_vertical(board, row, col, checker) or
                check_diagonal(board, row, col, checker)):
                return True
    return False

def check_horizontal(board, row, col, checker):
    """Check for horizontal win."""
    if col + 3 < COLUMNS:
        return all(board[row][col + i] == checker for i in range(4))
    return False

def check_vertical(board, row, col, checker):
    """Check for vertical win."""
    if row + 3 < ROWS:
        return all(board[row + i][col] == checker for i in range(4))
    return False

def check_diagonal(board, row, col, checker):
    """Check for diagonal win."""
    # Check for diagonal descending right
    if row + 3 < ROWS and col + 3 < COLUMNS:
        if all(board[row + i][col + i] == checker for i in range(4)):
            return True

    # Check for diagonal ascending right
    if row - 3 >= 0 and col + 3 < COLUMNS:
        if all(board[row - i][col + i] == checker for i in range(4)):
            return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    """Main game loop."""
    board = create_board()
    random_player_index = random.randint(0, len(PLAYERS) - 1)
    current_player_index = random_player_index

    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player_index]}, please enter a column (A-G): ")
        column = input().strip().upper()

        while not is_valid_input(column, board):
            print("Invalid input. Please choose a valid column (A-G): ")
            column = input().strip().upper()

        drop_checker(board, column, PLAYERS[current_player_index])

        if check_winner(board, PLAYERS[current_player_index]):
            print_board(board)
            print(f"Player {PLAYERS[current_player_index]} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
