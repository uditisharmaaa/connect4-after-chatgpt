import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can change this for more players

def create_board():
    """Creates a 2D board initialized with whitespaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels A-G
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def is_valid_input(column):
    """Checks if the input column is valid."""
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    """Returns the index of the column based on the letter input."""
    return ord(column) - 65

def drop_checker(board, column, player):
    """Drops the player's checker in the specified column."""
    for row in reversed(board):
        if row[get_column_index(column)] == ' ':
            row[get_column_index(column)] = player
            return True
    return False  # Column is full

def check_win(board):
    """Checks if there is a winner."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] != ' ' and all(board[r][c] == board[r][c + i] for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] != ' ' and all(board[r][c] == board[r + i][c] for i in range(4)):
                return True

    # Check diagonal (bottom left to top right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] != ' ' and all(board[r][c] == board[r + i][c + i] for i in range(4)):
                return True

    # Check diagonal (top left to bottom right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] != ' ' and all(board[r][c] == board[r - i][c + i] for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ").upper()

        # Validate input
        while not is_valid_input(column):
            column = input("Invalid input. Please enter a valid column (A-G): ").upper()

        # Try to drop the checker
        if not drop_checker(board, column, current_player):
            print("Column is full! Try again.")
            continue

        # Check for win
        if check_win(board):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch players
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
