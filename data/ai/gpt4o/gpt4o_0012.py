import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Display the board
def display_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check for a win
def is_winner(board, player):
    # Check horizontal, vertical, and two diagonal directions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_direction(board, player, row, col, 0, 1) or
                check_direction(board, player, row, col, 1, 0) or
                check_direction(board, player, row, col, 1, 1) or
                check_direction(board, player, row, col, 1, -1)):
                return True
    return False

# Check for four in a row in a specific direction
def check_direction(board, player, start_row, start_col, delta_row, delta_col):
    for i in range(4):
        row = start_row + i * delta_row
        col = start_col + i * delta_col
        if row < 0 or row >= ROWS or col < 0 or col >= COLUMNS or board[row][col] != player:
            return False
    return True

# Check for a draw
def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Drop a checker into a column
def drop_checker(board, player, column):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return True
    return False

# Validate user input
def get_valid_input():
    while True:
        column_input = input(f"Please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(65 + COLUMNS - 1):
            column_index = ord(column_input) - 65
            if any(board[row][column_index] == ' ' for row in range(ROWS)):
                return column_index
            else:
                print("Column is full, choose another column.")
        else:
            print("Invalid input, please try again.")

# Main game loop
def connect_4():
    board = initialize_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    display_board(board)

    while True:
        current_player = CHECKERS[current_player_index]
        print(f"Player {current_player}, it's your turn.")
        
        column = get_valid_input()
        if not drop_checker(board, current_player, column):
            print("Column is full, choose another column.")
            continue

        display_board(board)
        
        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    connect_4()
