import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    print("  A B C D E F G")
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_player_turn(players, current_player):
    """Return the current player's checker."""
    return CHECKERS[players.index(current_player)]

def get_next_player(players, current_player):
    """Return the next player in the list."""
    index = players.index(current_player)
    return players[(index + 1) % len(players)]

def is_valid_input(column):
    """Check if the input is a valid column label."""
    return column.upper() in "ABCDEFG"

def get_column_index(column):
    """Return the column index corresponding to the column label."""
    return ord(column.upper()) - ord("A")

def is_column_full(board, column):
    """Check if the column is full."""
    return board[0][column]!= " "

def get_available_row(board, column):
    """Return the available row index in the column."""
    for i in range(ROWS - 1, -1, -1):
        if board[i][column] == " ":
            return i

def place_checker(board, column, checker):
    """Place the checker in the available row in the column."""
    row = get_available_row(board, column)
    board[row][column] = checker

def check_win(board, checker):
    """Check if the player has won."""
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = [f"Player {CHECKERS[i]}" for i in range(PLAYERS)]
    current_player = random.choice(players)

    while True:
        os.system("clear")
        print_board(board)
        print(f"{current_player}, please enter a column:")

        column = input().strip()
        while not is_valid_input(column):
            print("Invalid input. Please enter a column label (A-G):")
            column = input().strip()

        column_index = get_column_index(column)
        if is_column_full(board, column_index):
            print("Column is full. Please try again.")
            continue

        checker = get_player_turn(players, current_player)
        place_checker(board, column_index, checker)

        if check_win(board, checker):
            os.system("clear")
            print_board(board)
            print(f"{current_player} won!")
            break

        if is_draw(board):
            os.system("clear")
            print_board(board)
            print("It's a draw!")
            break

        current_player = get_next_player(players, current_player)

if __name__ == "__main__":
    main()
