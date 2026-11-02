import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def initialize_board(rows, columns):
    """Creates and returns an empty board with given dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    letters = [chr(65 + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def check_win(board, symbol):
    """Checks if the given player (symbol) has won."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def drop_checker(board, column, symbol):
    """Drops a checker for the given player at the given column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return True
    return False

def main():
    # Configuration
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]
    board = initialize_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        move = input().strip().upper()
        if len(move) != 1 or not ('A' <= move <= chr(65 + COLUMNS - 1)):
            print("Invalid column. Try again.")
            continue

        column = ord(move) - 65
        if not drop_checker(board, column, current_player):
            print("Column is full. Try again.")
            continue

        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
