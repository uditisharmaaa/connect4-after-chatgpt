import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column letters
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print('+---' * COLS + '+')

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    letter = column.upper()
    return letter.isalpha() and ord(letter) - 65 < COLS

def get_column_index(column):
    """Convert column letter to index (0-based)."""
    return ord(column.upper()) - 65

def place_checker(board, column, checker):
    """Place the checker in the specified column.
    Returns True if placement was successful, False otherwise."""
    col_idx = get_column_index(column)
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
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
    """Check if the game is a draw (no more moves possible)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        # Get column input from player
        column = input(f"Player {current_player}, please enter a column: ").strip()
        
        # Validate input
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        
        col_idx = get_column_index(column)
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        # Place checker
        if place_checker(board, column, current_player):
            # Print updated board
            print_board(board)
            
            # Check for win
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            # Check for draw
            if is_draw(board):
                print("Game ended in a draw!")
                break
            
            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
