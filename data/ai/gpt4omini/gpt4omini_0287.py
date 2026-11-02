import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board():
    """Creates an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def valid_input(column):
    """Checks if the input column is valid."""
    return column.isalpha() and len(column) == 1 and 'A' <= column.upper() <= chr(65 + COLUMNS - 1)

def find_empty_row(board, col):
    """Finds the lowest empty row in the given column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, player, col):
    """Places the player's checker in the specified column."""
    row = find_empty_row(board, col)
    if row != -1:
        board[row][col] = player
        return True
    return False

def check_winner(board, player):
    """Checks if the specified player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    # Randomly select the starting player
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        while True:
            column = input().strip().upper()
            if valid_input(column):
                col_index = ord(column) - 65
                if place_checker(board, current_player, col_index):
                    break
                else:
                    print("Column is full, please select another column.")
            else:
                print("Invalid input, please enter a valid column (A-G).")

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
