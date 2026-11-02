import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def initialize_board():
    """Initialize and return an empty board with whitespaces."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the board in the specified format."""
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(65 + i) for i in range(NUM_COLS)]))
    
    # Print the board rows with borders
    for row in board:
        print("+" + "---+" * NUM_COLS)
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    
    print("+" + "---+" * NUM_COLS)

def is_valid_column(column):
    """Check if the input column is valid (a single uppercase letter within range)."""
    if len(column) != 1:
        return False
    
    col_char = column[0]
    return 'A' <= col_char <= chr(65 + NUM_COLS - 1)

def get_column_index(column):
    """Convert column letter (A, B, ...) to a zero-based index."""
    return ord(column[0].upper()) - ord('A')

def place_checker(board, column, checker):
    """
    Place the checker in the specified column at the lowest available row.
    Return True if successful, False otherwise (column full).
    """
    col_index = get_column_index(column)
    
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the given checker has four in a row (horizontally, vertically, or diagonally)."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row - 1][col + 1] == checker and 
                board[row - 2][col + 2] == checker and 
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for row in board:
        if " " in row:
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    # Initialize game
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    clear_screen()
    print_board(board)
    
    # Main game loop
    while True:
        player_checker = checkers[current_player]
        print(f"Player {player_checker}, please enter a column: ", end="")
        column = input().strip().upper()
        
        # Validate input
        if not is_valid_column(column):
            print("Invalid input. Please enter a column letter (A-G).")
            continue
        
        # Place checker and check if column was full
        if not place_checker(board, column, player_checker):
            print("That column is full. Please choose another column.")
            continue
        
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
