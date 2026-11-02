import os
import random

# Constants for game settings
ROWS = 6
COLUMNS = 7
CHECKER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # These symbols will allow for up to 5 players.
NUM_PLAYERS = 2  # Number of players for the game.

def create_board(rows, columns):
    """Initialize the game board with whitespace."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print('+' + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print('+' + "---+" * COLUMNS)

def is_valid_input(user_input, columns):
    """Check if the user's input is valid."""
    if len(user_input) != 1:
        return False
    column = ord(user_input.upper()) - ord('A')
    return 0 <= column < columns

def get_lowest_empty_row(board, column):
    """Get the lowest empty row for a given column."""
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            return row
    return None

def place_checker(board, column, symbol):
    """Place a checker on the board at the specified column."""
    row = get_lowest_empty_row(board, column)
    if row is not None:
        board[row][column] = symbol
        return True
    return False

def check_winner(board, symbol):
    """Check if a player has won the game."""
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the board is full."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(range(NUM_PLAYERS))
    print_board(board)

    while True:
        print(f"Player {CHECKER_SYMBOLS[current_player]}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_input(user_input, COLUMNS):
            print("Invalid input, please enter a valid column letter.")
            continue

        column = ord(user_input) - ord('A')
        if not place_checker(board, column, CHECKER_SYMBOLS[current_player]):
            print("Column is full, please choose another column.")
            continue

        print_board(board)

        if check_winner(board, CHECKER_SYMBOLS[current_player]):
            print(f"Player {CHECKER_SYMBOLS[current_player]} won!")
            break

        if check_draw(board):
            print("Game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
