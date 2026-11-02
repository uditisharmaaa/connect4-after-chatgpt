import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows with borders
    for row in board:
        print("+" + "---+".join(["" for _ in range(COLS)]) + "+")
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    
    # Print the bottom border
    print("+" + "---+".join(["" for _ in range(COLS)]) + "+")

def is_valid_column(col_input):
    """Check if the column input is valid (A, B, C, ...)."""
    if len(col_input) != 1:
        return False
    col_char = col_input.upper()
    return col_char.isalpha() and ord(col_char) - ord('A') < COLS

def get_column_index(col_input):
    """Convert column letter to index (A->0, B->1, ...)."""
    return ord(col_input.upper()) - ord('A')

def place_checker(board, player_symbol, col_idx):
    """Place the checker in the specified column if possible."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_symbol
            return True
    return False  # Column is full

def check_win(board, player_symbol):
    """Check if the current player has a winning configuration."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player_symbol and 
                board[row][col+1] == player_symbol and 
                board[row][col+2] == player_symbol and 
                board[row][col+3] == player_symbol):
                return True
    
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player_symbol and 
                board[row+1][col] == player_symbol and 
                board[row+2][col] == player_symbol and 
                board[row+3][col] == player_symbol):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player_symbol and 
                board[row+1][col+1] == player_symbol and 
                board[row+2][col+2] == player_symbol and 
                board[row+3][col+3] == player_symbol):
                return True
    
    # Check diagonally (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player_symbol and 
                board[row-1][col+1] == player_symbol and 
                board[row-2][col+2] == player_symbol and 
                board[row-3][col+3] == player_symbol):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ", end="")
        col_input = input().strip()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a column letter (A to G).")
            input("Press Enter to continue...")
            continue
        
        col_idx = get_column_index(col_input)
        
        if not place_checker(board, current_player, col_idx):
            print("Column is full. Try another column.")
            input("Press Enter to continue...")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    play_game()
