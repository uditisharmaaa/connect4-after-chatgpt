import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print board rows
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_input(col_input):
    if len(col_input) != 1:
        return False
    col = ord(col_input.upper()) - ord('A')
    return 0 <= col < COLS

def place_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ", end="")
        
        col_input = input().strip().upper()
        
        if not is_valid_input(col_input):
            print("Invalid input! Please try again with a valid column (A-G).")
            continue
        
        col = ord(col_input) - ord('A')
        
        if not place_checker(board, col, current_player):
            print("Column is full! You lose your turn.")
        else:
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
