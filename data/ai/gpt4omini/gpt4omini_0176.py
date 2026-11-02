import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Add more players if needed like ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates the Connect 4 board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the Connect 4 board."""
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+" + "---+" * COLS)
    for row in reversed(board):
        print("|", " | ".join(row), "|")
        print("+" + "---+" * COLS)
    print()

def is_valid_column(column):
    """Checks if the chosen column is valid."""
    return 0 <= column < COLS

def is_column_full(board, column):
    """Checks if the chosen column is full."""
    return board[ROWS - 1][column] != ' '

def place_checker(board, column, checker):
    """Places a checker in the specified column."""
    for row in range(ROWS):
        if board[row][column] == ' ':
            board[row][column] = checker
            break

def check_winner(board, checker):
    """Checks for four in a row for the given checker."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is full and there is no winner."""
    return all(board[ROWS - 1][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)  # Random first player
    moves = 0
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column_input = input().upper()

        if len(column_input) != 1 or not ('A' <= column_input <= chr(65 + COLS - 1)):
            print("Invalid input. Please enter a letter between A and " + chr(65 + COLS - 1))
            continue  # Resend input

        column = ord(column_input) - 65  # Convert column letter to index

        if not is_valid_column(column):
            print("Column is out of range. Please choose a valid column.")
            continue  # Resend input

        if is_column_full(board, column):
            print("Column is full. You lose your turn.")
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
            continue  # Resend input

        place_checker(board, column, current_player)
        moves += 1
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
