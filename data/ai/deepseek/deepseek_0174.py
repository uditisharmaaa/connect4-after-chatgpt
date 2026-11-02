import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Number of players (2-5)

# Players' checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    """Create a new empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print the column headers
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    
    # Print each row with separators
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print the bottom border
    print('+' + '---+' * COLS)

def get_valid_column(current_player):
    """Ask the current player for a column until a valid input is provided."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col_idx = ord(column) - ord('A')
        if col_idx < 0 or col_idx >= COLS:
            print(f"Column must be between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col_idx

def place_checker(board, col_idx, checker):
    """Place the checker in the specified column if possible."""
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False  # Column is full

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
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(CHECKERS)
    
    while True:
        print_board(board)
        col_idx = get_valid_column(current_player)
        
        if not place_checker(board, col_idx, current_player):
            print("Column is full. You lose your turn.")
        else:
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            
            if is_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                break
        
        # Switch to the next player
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
