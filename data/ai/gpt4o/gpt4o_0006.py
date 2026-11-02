import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def init_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Use 'cls' on Windows
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Place a checker in the column
def place_checker(board, column, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == " ":
            board[r][column] = player
            return True
    return False

# Validate user input
def is_valid_input(input_str, cols):
    return input_str.isalpha() and len(input_str) == 1 and 0 <= ord(input_str) - ord('A') < cols

# Main game loop
def play_game():
    board = init_board(ROWS, COLS)
    players = CHECKERS[:PLAYER_COUNT]
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)
    
    while True:
        current_player = players[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            input_str = input().strip().upper()
            if is_valid_input(input_str, COLS):
                column = ord(input_str) - ord('A')
                if place_checker(board, column, current_player):
                    break
                else:
                    print("Column full. Please try a different column.")
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

play_game()
