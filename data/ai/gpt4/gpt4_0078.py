import os
import random

# Global constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checker symbols for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates the Connect 4 board filled with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the Connect 4 board."""
    # Print column labels
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print("+---" * COLUMNS + "+")
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if a column is valid for a move."""
    return column in range(COLUMNS) and board[0][column] == " "

def get_next_open_row(board, column):
    """Returns the next open row for a checker in the given column."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == " ":
            return r
    return -1  # If the column is full

def make_move(board, column, checker):
    """Places the checker in the specified column."""
    row = get_next_open_row(board, column)
    if row != -1:
        board[row][column] = checker

def check_win(board, checker):
    """Checks for a win condition (4 in a row horizontally, vertically, diagonally)."""
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

    return False

def is_draw(board):
    """Checks if the board is completely filled, resulting in a draw."""
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def get_column_input():
    """Prompts the player for a valid column input."""
    while True:
        try:
            column_letter = input("Please enter a column: ").upper()
            column = ord(column_letter) - 65
            if 0 <= column < COLUMNS:
                return column
            raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid column (A-G).")

def main():
    # Initialize the game
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    clear_screen()
    print_board(board)
    print(f"Player {current_player} starts!")

    while True:
        print(f"Player {current_player}, it's your turn.")
        column = get_column_input()

        if is_valid_column(column, board):
            make_move(board, column, current_player)

            clear_screen()
            print_board(board)

            # Check for win
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break

            # Check for draw
            if is_draw(board):
                print("The game is a draw!")
                break

            # Switch to the next player
            current_player = players[(players.index(current_player) + 1) % PLAYERS]
        else:
            print("Column is full or invalid. Try again.")

if __name__ == "__main__":
    main()
