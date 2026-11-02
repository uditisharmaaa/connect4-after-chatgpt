import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Initialize the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for valid input
def is_valid_input(col_input):
    return col_input.isalpha() and len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + COLS - 1)

# Place the checker in the board
def place_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom of the column
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

# Check for win condition
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal (both directions)
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                if check_direction(board, row, col, checker, 1, 0) or \
                   check_direction(board, row, col, checker, 0, 1) or \
                   check_direction(board, row, col, checker, 1, 1) or \
                   check_direction(board, row, col, checker, 1, -1):
                    return True
    return False

# Helper function to check in a specific direction
def check_direction(board, row, col, checker, delta_row, delta_col):
    count = 0
    for i in range(4):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

# Check for a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main game loop
def connect4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    print_board(board)
    
    while not game_over:
        current_player = PLAYERS[current_player_index]
        input_valid = False

        while not input_valid:
            col_input = input(f"Player {current_player}, please enter a column: ").upper()
            if is_valid_input(col_input):
                column = ord(col_input) - ord('A')
                if place_checker(board, column, current_player):
                    input_valid = True
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a letter corresponding to a column (A-G).")

        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True

        current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    connect4()
