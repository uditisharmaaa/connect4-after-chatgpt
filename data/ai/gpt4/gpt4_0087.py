import os
import random

# Constants
NUM_PLAYERS = 2  # Change this to 3, 4, or 5 for more players
ROWS = 6
COLS = 7
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    col_headers = "  " + "   ".join(chr(i + 65) for i in range(COLS))
    print(col_headers)
    print("+---" * COLS + "+")
    
    # Print rows of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_column_index(input_char):
    if input_char.isalpha() and len(input_char) == 1:
        col_index = ord(input_char.upper()) - 65
        if 0 <= col_index < COLS:
            return col_index
    return -1

def is_column_full(board, col):
    return board[0][col] != " "

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return

def is_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + offset] == player for offset in range(4)):
                return True
                
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + offset][col] == player for offset in range(4)):
                return True
                
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + offset][col + offset] == player for offset in range(4)):
                return True
                
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - offset][col + offset] == player for offset in range(4)):
                return True
                
    return False

def is_draw(board):
    return all(is_column_full(board, col) for col in range(COLS))

def connect_4():
    # Initialize the game
    board = initialize_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    clear_screen()
    print("Welcome to Connect 4!")
    print_board(board)
    
    # Game loop
    while True:
        current_player = PLAYER_CHECKERS[current_player_idx]
        print(f"Player {current_player}, it's your turn!")
        column = -1
        
        # Get valid input from the player
        while column == -1:
            user_input = input("Please enter a column (A-G): ").strip()
            column = get_column_index(user_input)
            
            if column == -1:
                print("Invalid input! Please enter a valid column letter.")
            elif is_column_full(board, column):
                print("Column is full! Choose another column.")
                column = -1
        
        # Place the checker
        drop_checker(board, column, current_player)
        clear_screen()
        print_board(board)
        
        # Check for a win
        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    connect_4()
