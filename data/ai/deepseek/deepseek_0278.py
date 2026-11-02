import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create and return an empty board with given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print the board rows with separators
    for row in board:
        print('+---+' * BOARD_COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * BOARD_COLS)

def is_valid_column(col_input):
    """Check if the provided column input is valid."""
    if len(col_input) != 1:
        return False
    col = ord(col_input.upper()) - ord('A')
    return 0 <= col < BOARD_COLS

def place_checker(board, col, checker):
    """
    Place the checker in the specified column if possible.
    Returns True if placement is successful, False otherwise.
    """
    col_idx = ord(col.upper()) - ord('A')
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has a winning condition."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a column letter (A-G).")
            continue
        
        if not place_checker(board, col_input, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
