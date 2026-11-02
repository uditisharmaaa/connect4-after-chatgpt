import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with NUM_ROWS rows and NUM_COLS columns."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(65 + i) for i in range(NUM_COLS)) + "  "
    print(header)
    
    # Print the board rows with borders
    for row in board:
        border = "+".join(["---"] * NUM_COLS)
        print(f"+{border}+")
        print("| " + " | ".join(row) + " |")
    
    # Print the bottom border
    border = "+".join(["---"] * NUM_COLS)
    print(f"+{border}+")

def get_valid_column(board, player):
    """Prompt the player to input a valid column and return its index."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= NUM_COLS:
            print(f"Invalid column. Please choose a letter from A to {chr(65 + NUM_COLS - 1)}.")
            continue
        
        if board[0][col] != " ":
            print("Column is full. Choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return

def check_win(board, player):
    """Check if the player has won the game."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and
                board[row][col+1] == player and
                board[row][col+2] == player and
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == player and
                board[row+1][col] == player and
                board[row+2][col] == player and
                board[row+3][col] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and
                board[row+1][col+1] == player and
                board[row+2][col+2] == player and
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(NUM_ROWS - 3):
        for col in range(3, NUM_COLS):
            if (board[row][col] == player and
                board[row+1][col-1] == player and
                board[row+2][col-2] == player and
                board[row+3][col-3] == player):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn")
        
        col = get_valid_column(board, current_player)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
