import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create and return an empty board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing the updated board
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows with separators
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    
    print('+---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid (a letter within board bounds)."""
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    """Convert a column letter (A, B, etc.) to a zero-based index."""
    return ord(col.upper()) - ord('A')

def drop_checker(board, col, checker):
    """
    Attempt to drop a checker into the specified column.
    Returns the row where the checker was placed, or None if column is full.
    """
    col_idx = get_column_index(col)
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx
    return None

def check_win(board, row, col, checker):
    """
    Check if the latest move at (row, col) resulted in a win.
    Returns True if there are four consecutive checkers in any direction.
    """
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check if count meets the win condition
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is completely filled with checkers."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        
        print(f"Player {current_player}, please enter a column: ", end='')
        col = input().strip().upper()
        
        # Validate input
        if not is_valid_column(col):
            print(f"Invalid input. Please enter a column from A to {chr(65 + COLS - 1)}.")
            continue
        
        # Attempt to place the checker
        col_idx = get_column_index(col)
        row = drop_checker(board, col, current_player)
        if row is None:
            print(f"Column {col} is full. You lose your turn.")
        else:
            # Check for win
            if check_win(board, row, col_idx, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            # Check for draw
            if is_board_full(board):
                print_board(board)
                print("The game is a draw!")
                break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
