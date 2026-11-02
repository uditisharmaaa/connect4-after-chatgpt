import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Number of players (default: 2)
WIN_LENGTH = 4  # Number of checkers in a row needed to win

def create_board(rows, cols):
    """Creates a game board with the given dimensions as a 2D list."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board to the console with column letters."""
    os.system("clear")
    print("  " + "   ".join(chr(65 + col) for col in range(len(board[0]))))  # Column labels (A, B, ...)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Checks if a column is valid and has space available."""
    return column in range(len(board[0])) and board[0][column] == " "

def get_lowest_row(column, board):
    """Gets the lowest available row in the column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return -1

def drop_checker(column, checker, board):
    """Drops a checker into a column."""
    row = get_lowest_row(column, board)
    if row != -1:
        board[row][column] = checker
        return True
    return False

def is_win(board, checker):
    """Checks if the given checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def is_draw(board):
    """Checks if the game is a draw (no empty spaces left)."""
    return all(cell != " " for row in board for cell in row)

def get_column_input(board):
    """Prompts the player for a valid column input."""
    while True:
        column_input = input("Please enter a column: ").upper()
        if len(column_input) == 1 and "A" <= column_input <= chr(65 + len(board[0]) - 1):
            column = ord(column_input) - 65
            if is_valid_column(column, board):
                return column
            else:
                print("Column is full. Try another one.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def main():
    """Main function to run the Connect 4 game."""
    # Create the game board
    board = create_board(ROWS, COLUMNS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player_index]}'s turn.")
        column = get_column_input(board)

        # Place the checker
        drop_checker(column, PLAYERS[current_player_index], board)

        # Check for win or draw
        if is_win(board, PLAYERS[current_player_index]):
            print_board(board)
            print(f"Player {PLAYERS[current_player_index]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
