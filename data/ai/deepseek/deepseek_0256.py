import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create an empty game board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column letters
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + ('---+' * COLS))

def get_valid_column_input(current_player):
    """Get a valid column input from the current player."""
    valid_columns = [chr(65 + i) for i in range(COLS)]
    while True:
        column_input = input(f"Player {current_player}, please enter a column: ").upper()
        if column_input in valid_columns:
            return ord(column_input) - 65  # Convert to column index (0-based)
        print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")

def place_checker(board, column, checker):
    """Place the checker in the specified column if possible."""
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker
            ):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (
                board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker
            ):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (
                board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker
            ):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker
            ):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    os.system('clear')
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        column = get_valid_column_input(current_player)
        if not place_checker(board, column, current_player):
            print(f"Column {chr(65 + column)} is full. Player {current_player} loses their turn.")
        
        os.system('clear')
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
