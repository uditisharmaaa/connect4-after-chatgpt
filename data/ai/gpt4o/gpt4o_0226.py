import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for players

def create_board():
    """Initialize a game board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def select_random_player():
    """Select a random player to start the game."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_input(column):
    """Check if the user input is a valid column letter."""
    return column.isalpha() and ord(column.upper()) - 65 < COLUMNS

def is_column_full(board, column_index):
    """Check if the column is completely full."""
    return board[0][column_index] != " "

def place_checker(board, column_index, symbol):
    """Place a checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = symbol
            break

def check_win(board, symbol):
    """Check for a win condition: 4 symbols in a row."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    """Start and manage the Connect 4 game."""
    board = create_board()
    current_player = select_random_player()
    print_board(board)

    while True:
        symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {symbol}, please enter a column:")

        # Get and validate player input
        while True:
            try:
                column = input().strip().upper()
                if not is_valid_input(column):
                    raise ValueError("Invalid input. Please enter a valid column letter.")

                column_index = ord(column) - 65
                if is_column_full(board, column_index):
                    print("Column is full, invalid move. Try another column.")
                    continue

                break
            except ValueError as e:
                print(e)

        # Place the checker on the board
        place_checker(board, column_index, symbol)
        print_board(board)

        # Check for winning condition
        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            break

        # Check for draw condition
        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate players
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
