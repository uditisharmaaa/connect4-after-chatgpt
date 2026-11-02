import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    """Create a 2D board with all elements initialized to whitespaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    """Print the Connect 4 board."""
    print("  " + " ".join(string.ascii_uppercase[:columns]))
    for row in board:
        print("+---" * columns + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * columns + "+")

def validate_input(column, columns):
    """Validate the user input."""
    if not column.isalpha():
        return False
    if column.upper() not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column(board, column):
    """Get the column index from the user input."""
    return ord(column.upper()) - 65

def place_checker(board, column, row, checker):
    """Place the checker in the specified column and row."""
    board[row][column] = checker

def check_win(board, checker):
    """Check if the player has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == checker:
                return True

    # Check vertical
    for column in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][column] == board[i + 1][column] == board[i + 2][column] == board[i + 3][column] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for column in range(len(board[0]) - 3):
            if board[row][column] == board[row + 1][column + 1] == board[row + 2][column + 2] == board[row + 3][column + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for column in range(len(board[0]) - 3):
            if board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] == board[row - 3][column + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)

    # Choose a random player to start
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(board, COLUMNS)
        print("Player", CHECKERS[current_player], "please enter a column:")

        # Get the column from the user
        while True:
            column = input()
            if validate_input(column, COLUMNS):
                break
            print("Invalid input. Please enter a letter between A and", string.ascii_uppercase[COLUMNS - 1])

        # Get the column index
        column_index = get_column(board, column)

        # Find the first available row
        for row in range(ROWS - 1, -1, -1):
            if board[row][column_index] == " ":
                place_checker(board, column_index, row, CHECKERS[current_player])
                break
        else:
            print("Column is full. Please try again.")
            continue

        # Check if the player has won
        if check_win(board, CHECKERS[current_player]):
            os.system('clear')
            print_board(board, COLUMNS)
            print("Player", CHECKERS[current_player], "won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            os.system('clear')
            print_board(board, COLUMNS)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
