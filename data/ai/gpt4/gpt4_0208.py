import os
import random

# Constants for configuration
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # This will dictate the number of players in the game

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def initialize_board():
    """Initializes the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board to the console."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Checks if the selected column is valid and not full."""
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == " "

def drop_checker(board, column, checker):
    """Drops a checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False  # Should never reach here if the column is valid

def check_for_win(board, player_checker):
    """Checks if a given player has won the game."""
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right) check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right) check
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def get_column_from_user(board):
    """Prompts the user to input a column and validates the input."""
    while True:
        column_input = input("Please enter a column: ").strip().upper()
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue

        column = ord(column_input) - 65
        if column < 0 or column >= COLS:
            print(f"Invalid column. Please choose between A and {chr(64 + COLS)}.")
            continue

        if not is_valid_column(column, board):
            print("Column is full or invalid. Choose another column.")
            continue

        return column

def main():
    board = initialize_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print("Welcome to Connect 4!")
    input("Press Enter to start the game...")

    while True:
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn!")

        column = get_column_from_user(board)
        drop_checker(board, column, current_player)

        if check_for_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
