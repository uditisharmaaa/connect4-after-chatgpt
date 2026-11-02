import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Max 5 players

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column labels A-G
    print("+" + "---+" * COLS)  # Print the top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Print the row border

def is_valid_input(column):
    """Check if the user input is valid (A-G)."""
    return column.isalpha() and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    """Convert column letter to its index (0-6)."""
    return ord(column) - 65

def is_column_full(board, col):
    """Check if a column is full."""
    return board[0][col] != " "

def drop_checker(board, col, marker):
    """Drop a player's checker into the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = marker
            return True
    return False

def check_win(board, marker):
    """Check for a win condition for the specified marker."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == marker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == marker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == marker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game board is full, resulting in a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Initialize game
    board = initialize_board()
    current_player = random.choice(range(len(PLAYERS)))  # Randomly select first player
    print_board(board)

    while True:
        marker = PLAYERS[current_player]
        column = input(f"Player {marker}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        # Validate input
        while not is_valid_input(column):
            column = input(f"Invalid input. Please enter a valid column (A-{chr(65 + COLS - 1)}): ").upper()

        col_index = get_column_index(column)

        if is_column_full(board, col_index):
            print("Column is full! Turn lost.")
        else:
            drop_checker(board, col_index, marker)
            print_board(board)

            if check_win(board, marker):
                print(f"Player {marker} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % len(PLAYERS)  # Switch player

if __name__ == "__main__":
    main()
