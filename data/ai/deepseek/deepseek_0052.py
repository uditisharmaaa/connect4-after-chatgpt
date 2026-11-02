import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column letters
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print("+" + "---+" * COLS)
    
    for row in board:
        # Print row content
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        # Print row border
        print("+" + "---+" * COLS)

def is_valid_column(col):
    """Check if the input column is valid."""
    if len(col) != 1:
        return False
    col_letter = col.upper()
    return col_letter >= 'A' and col_letter < chr(65 + COLS)

def drop_checker(board, col, player):
    """Place the player's checker in the specified column."""
    col_idx = ord(col.upper()) - ord('A')
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player
            return True
    return False  # Column is full

def check_winner(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == player and 
                board[row+1][col-1] == player and 
                board[row+2][col-2] == player and 
                board[row+3][col-3] == player):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if " " in row:
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    # Initialize game
    board = initialize_board()
    players = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
    current_player = random.choice(players)
    
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Player {current_player} goes first.")
    print_board(board)
    
    while True:
        # Get player input
        while True:
            col = input(f"Player {current_player}, please enter a column: ").strip()
            if is_valid_column(col):
                break
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
        
        # Attempt to place checker
        col_letter = col.upper()
        if drop_checker(board, col_letter, current_player):
            clear_screen()
            print_board(board)
            
            # Check for win
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                return
                
            # Check for draw
            if is_draw(board):
                print("The game is a draw!")
                return
                
            # Switch player
            current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]
        else:
            clear_screen()
            print_board(board)
            print(f"Column {col_letter} is full. Player {current_player} loses their turn.")
            current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
