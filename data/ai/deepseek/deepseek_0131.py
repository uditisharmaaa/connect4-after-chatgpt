import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

# Player symbols
SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Create and return an empty game board with the specified dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    
    # Print the board with borders
    border = "+" + ("---+" * len(board[0]))
    for row in board:
        print(border)
        print("| " + " | ".join(cell for cell in row) + " |")
    print(border)

def is_valid_column(board, col):
    """Check if the specified column (0-based index) is valid and has space."""
    if col < 0 or col >= len(board[0]):
        return False
    return board[0][col] == " "

def place_checker(board, col, symbol):
    """Place the player's symbol in the specified column (0-based index)."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return True
    return False

def check_win(board, symbol):
    """Check if the specified symbol has a winning line (4 in a row)."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    
    # Check vertical
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLS)
    players = SYMBOLS[:PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()
        
        if not user_input or len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col = ord(user_input) - ord('A')
        if not is_valid_column(board, col):
            print("Invalid column. Either the column is full or doesn't exist.")
            continue
        
        if place_checker(board, col, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                break
            
            # Switch to the next player
            current_player = players[(players.index(current_player) + 1) % len(players)]
        else:
            print("Column is full. Please try another column.")

if __name__ == "__main__":
    main()
