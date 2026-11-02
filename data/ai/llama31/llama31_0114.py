import os
import random

# Constants for board dimensions and players
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board with whitespace
def initialize_board():
    board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

# Print the board to the console
def print_board(board, current_player):
    # Clear the screen
    os.system('clear')
    
    # Print column labels
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    
    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---+---+---+---+---+---+---+")
    
    # Print current player's turn
    print(f"Player {current_player}, please enter a column:")

# Validate user input for column
def validate_input(input_str):
    # Check if input is an uppercase letter
    if len(input_str)!= 1 or not input_str.isalpha() or not input_str.isupper():
        return False
    
    # Check if input is within column range
    if ord(input_str) - ord('A') < 0 or ord(input_str) - ord('A') >= BOARD_COLUMNS:
        return False
    
    return True

# Place checker in column
def place_checker(board, column, checker):
    # Find the lowest available space in the column
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

# Check for win
def check_win(board, current_player):
    # Check horizontal wins
    for row in board:
        for col in range(BOARD_COLUMNS - 3):
            if row[col] == current_player and row[col + 1] == current_player and row[col + 2] == current_player and row[col + 3] == current_player:
                return True
    
    # Check vertical wins
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == current_player and board[row + 1][col] == current_player and board[row + 2][col] == current_player and board[row + 3][col] == current_player:
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == current_player and board[row + 1][col + 1] == current_player and board[row + 2][col + 2] == current_player and board[row + 3][col + 3] == current_player:
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == current_player and board[row - 1][col + 1] == current_player and board[row - 2][col + 2] == current_player and board[row - 3][col + 3] == current_player:
                return True
    
    return False

# Check for draw
def check_draw(board):
    # Check if all cells are filled
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def play_game():
    # Initialize board and players
    board = initialize_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = players[current_player_index]
    
    while True:
        # Print the board
        print_board(board, current_player)
        
        # Get user input for column
        while True:
            input_str = input()
            if validate_input(input_str):
                column = ord(input_str) - ord('A')
                break
            else:
                print("Invalid input. Please enter a column letter.")
        
        # Place checker in column
        place_checker(board, column, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board, current_player)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board, current_player)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = players[current_player_index]

play_game()
