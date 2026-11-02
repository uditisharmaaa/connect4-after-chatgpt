import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players; use first N checkers based on PLAYERS

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    # Print column letters
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    # Print board with grid
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Validate user input
def is_valid_input(column, board):
    if column.isalpha() and len(column) == 1:
        column = ord(column.upper()) - 65
        if 0 <= column < COLUMNS and board[0][column] == " ":
            return True
    return False

# Place the checker in the lowest available row of the chosen column
def place_checker(board, column, checker):
    col_index = ord(column.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

# Check for a win in all directions
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal (\ and /) directions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                col + 3 < COLUMNS and 
                all(board[row][col + i] == checker for i in range(4))
            ):  # Horizontal
                return True
            if (
                row + 3 < ROWS and 
                all(board[row + i][col] == checker for i in range(4))
            ):  # Vertical
                return True
            if (
                col + 3 < COLUMNS and row + 3 < ROWS and 
                all(board[row + i][col + i] == checker for i in range(4))
            ):  # Diagonal \
                return True
            if (
                col - 3 >= 0 and row + 3 < ROWS and 
                all(board[row + i][col - i] == checker for i in range(4))
            ):  # Diagonal /
                return True
    return False

# Check if the board is full
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main function to run the game
def connect4():
    board = create_board()
    current_players = CHECKERS[:PLAYERS]
    random.shuffle(current_players)
    
    # Randomly select starting player
    current_player = current_players[0]
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip()
        
        # Validate input
        while not is_valid_input(user_input, board):
            print("Invalid input. Please enter a valid column (A-G).")
            user_input = input().strip()
        
        # Place checker
        place_checker(board, user_input, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = current_players.index(current_player)
        current_player = current_players[(current_player_index + 1) % PLAYERS]

# Run the game
if __name__ == "__main__":
    connect4()
