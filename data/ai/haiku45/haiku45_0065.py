import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board with empty spaces
def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)} ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()

# Get valid input from player
def get_player_input(current_player_checker):
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
        
        # Check if input is valid
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if col < 0 or col >= COLS:
            print(f"Invalid input. Please enter a column between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col

# Place checker in the board
def place_checker(board, col, checker):
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False

# Check for horizontal win
def check_horizontal_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check for vertical win
def check_vertical_win(board, checker):
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check for diagonal win (top-left to bottom-right)
def check_diagonal_right_win(board, checker):
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check for diagonal win (top-right to bottom-left)
def check_diagonal_left_win(board, checker):
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check if there is a win
def check_win(board, checker):
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_right_win(board, checker) or 
            check_diagonal_left_win(board, checker))

# Check if the board is full
def is_board_full(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

# Main game loop
def play_game():
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player]
        
        # Get valid column input
        while True:
            col = get_player_input(current_checker)
            if place_checker(board, col, current_checker):
                break
        
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
