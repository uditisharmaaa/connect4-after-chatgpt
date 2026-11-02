import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Can expand this for 3-5 players if needed

# Function to create and initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to check if the input is valid
def is_valid_input(col_input):
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col_index = ord(col_input.upper()) - 65
    return 0 <= col_index < COLS

# Function to place the checker at the correct location
def place_checker(board, col_index, player):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player
            return True
    return False  # Column is full

# Function to check for a win
def check_win(board, player):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonal (\ direction)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonal (/ direction)
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4)):
                    return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main function to play the game
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()
        
        while not is_valid_input(col_input):
            col_input = input("Invalid input. Please enter a valid column (A-G): ").strip().upper()
        
        col_index = ord(col_input) - 65
        
        if not place_checker(board, col_index, current_player):
            print("Column is full! Try another column.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Start the game
if __name__ == "__main__":
    play_game()
