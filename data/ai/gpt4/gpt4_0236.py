import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

def create_board(rows, cols):
    """Create the game board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    column_headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(column_headers)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(input_char, num_columns):
    """Validate user input for column selection."""
    return len(input_char) == 1 and 'A' <= input_char <= chr(ord('A') + num_columns - 1)

def is_column_full(board, column_index):
    """Check if a column is full."""
    return board[0][column_index] != EMPTY_CELL

def drop_checker(board, column_index, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[column_index] == EMPTY_CELL:
            row[column_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != EMPTY_CELL for col in range(COLUMNS))

def main():
    # Initialize variables
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Set number of players (you can customize this to support up to MAX_PLAYERS)
    checkers = PLAYER_CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        current_checker = checkers[current_player_index]
        print(f"Player {current_checker}, it's your turn.")
        column_input = input("Please enter a column: ").strip().upper()

        if not is_valid_input(column_input, COLUMNS):
            print("Invalid input! Please enter a valid column letter.")
            continue

        column_index = ord(column_input) - ord('A')

        if is_column_full(board, column_index):
            print("Column is full! Please choose a different column.")
            continue

        # Drop checker and update board
        drop_checker(board, column_index, current_checker)
        print_board(board)

        # Check for a win or draw
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
