import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Function to create the initial game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the current game board
def print_board(board):
    os.system('clear')
    column_labels = "  ".join([chr(ord('A') + i) for i in range(COLUMNS)])
    print(f"  {column_labels}")
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Function to check for a win condition
def check_win(board, symbol):
    # Check horizontal, vertical, and diagonal (both directions) for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_line(board, row, col, 0, 1, symbol) or
                check_line(board, row, col, 1, 0, symbol) or
                check_line(board, row, col, 1, 1, symbol) or
                check_line(board, row, col, 1, -1, symbol)):
                return True
    return False

# Helper function for checking lines for a win
def check_line(board, start_row, start_col, delta_row, delta_col, symbol):
    count = 0
    for i in range(4):
        row = start_row + i * delta_row
        col = start_col + i * delta_col
        if 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == symbol:
            count += 1
        else:
            break
    return count == 4

# Function to check for a draw condition
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Function to get a valid column choice from the player
def get_valid_column(board):
    while True:
        column_input = input("Please enter a column: ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + COLUMNS - 1):
            column = ord(column_input) - ord('A')
            if board[0][column] == " ":
                return column
        print("Invalid input. Try again.")

# Function to place a checker in the chosen column
def place_checker(board, player_symbol, column):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = player_symbol
            return

# Main game loop
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {PLAYER_SYMBOLS[current_player]}'s turn.")
        
        column = get_valid_column(board)
        place_checker(board, PLAYER_SYMBOLS[current_player], column)

        if check_win(board, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
