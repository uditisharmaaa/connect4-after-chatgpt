import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

# Initialize the board
def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLS)  # Row border
    print(f"Player {current_player}, please enter a column:")  # Player prompt

# Check if the input column is valid
def is_valid_input(column_string):
    if len(column_string) != 1 or not 'A' <= column_string <= 'G':
        return False
    col_index = ord(column_string) - 65
    return 0 <= col_index < COLS

# Place the checker in the board
def place_checker(board, column):
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = current_player
            return True
    return False  # Column is full

# Check for a win condition
def check_win(board, player):
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                if check_direction(board, row, col, player, 1, 0) or \
                   check_direction(board, row, col, player, 0, 1) or \
                   check_direction(board, row, col, player, 1, 1) or \
                   check_direction(board, row, col, player, 1, -1):
                    return True
    return False

# Check in a specific direction for winning condition
def check_direction(board, start_row, start_col, player, delta_row, delta_col):
    count = 0
    for i in range(4):
        row = start_row + i * delta_row
        col = start_col + i * delta_col
        if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
            count += 1
        else:
            break
    return count == 4

# Check for a draw
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS)  # Randomly select the first player
    print_board(board)

    while True:
        valid_input = False
        
        while not valid_input:
            user_input = input().upper()
            if is_valid_input(user_input):
                valid_input = place_checker(board, user_input)
                if not valid_input:
                    print("Column is full! Choose another column:")
            else:
                print("Invalid input! Please enter a column (A-G):")
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % len(PLAYERS)]

# Start the game
if __name__ == "__main__":
    play_game()
