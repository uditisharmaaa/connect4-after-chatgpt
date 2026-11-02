import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First N players

def initialize_board():
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print(' ' + '   '.join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    
    # Print the board rows with separators
    for row in board:
        print('+' + '---+' * NUM_COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print the bottom border
    print('+' + '---+' * NUM_COLS)

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return 'A' <= col_char <= chr(ord('A') + NUM_COLS - 1)

def place_checker(board, column, checker):
    """Place the checker in the specified column if possible.
    Returns True if successful, False otherwise."""
    col_idx = ord(column.upper()) - ord('A')
    
    # Check if column is full
    if board[0][col_idx] != ' ':
        return False
    
    # Find the lowest empty row
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal, vertical, and both diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == checker:
                for dr, dc in directions:
                    count = 1
                    for step in range(1, 4):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        current_player = PLAYERS[current_player_idx]
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        column = input().strip().upper()
        
        # Validate input
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        # Try to place checker
        if not place_checker(board, column, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
