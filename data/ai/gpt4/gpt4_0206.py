import os
import random

# Constants for board dimensions and number of players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Player checkers in sequence
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

# Clear screen function
def clear_screen():
    os.system('clear')

# Initialize the game board
def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the game board
def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check valid input
def valid_input(column, board):
    if column.isalpha() and len(column) == 1:  # Must be a single letter
        col_index = ord(column.upper()) - 65
        if 0 <= col_index < len(board[0]) and board[0][col_index] == " ":
            return True
    return False

# Place the checker in the selected column
def place_checker(column, board, checker):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

# Check if the player wins (horizontal, vertical, diagonal)
def check_winner(board, checker):
    # Horizontal check
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

# Check if the board is full (draw)
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main game loop
def play_game():
    board = initialize_board(NUM_ROWS, NUM_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Randomly selected Player {CHECKERS[current_player]} to start!")

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip()

        if valid_input(column, board):
            place_checker(column, board, CHECKERS[current_player])

            if check_winner(board, CHECKERS[current_player]):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Invalid input. Please try again.")

# Run the game
if __name__ == "__main__":
    play_game()
