import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Set this to the number of players (2-5)

def clear_screen():
    """Clears the screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    col_labels = " ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Checks if the input column is valid."""
    return column.isalpha() and len(column) == 1 and 0 <= ord(column.upper()) - 65 < len(board[0])

def is_column_full(column, board):
    """Checks if the column is full."""
    col_index = ord(column.upper()) - 65
    return all(row[col_index] != " " for row in board)

def drop_checker(column, symbol, board):
    """Places the checker in the correct position."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = symbol
            break

def check_winner(board, symbol):
    """Checks for victory conditions."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == symbol for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r+i][c] == symbol for i in range(4)):
                return True

    # Check diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == symbol for i in range(4)):
                return True

    # Check diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game results in a draw."""
    return all(cell != " " for row in board for cell in row)

def connect4():
    """Main function to run the Connect 4 game."""
    clear_screen()
    board = create_board(ROWS, COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print(f"Welcome to Connect 4!\n")
    print_board(board)

    while True:
        print(f"Player {players[current_player]}, it's your turn!")
        column = input("Please enter a column (A-G): ").strip()

        # Validate input
        while not is_valid_column(column, board) or is_column_full(column, board):
            print("Invalid input! Please try again.")
            column = input("Please enter a column (A-G): ").strip()

        # Place the checker
        drop_checker(column, players[current_player], board)

        clear_screen()
        print_board(board)

        # Check for winner
        if check_winner(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect4()
