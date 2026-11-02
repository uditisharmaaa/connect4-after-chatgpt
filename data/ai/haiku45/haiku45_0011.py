"""
Connect 4 Game Implementation
A two-player (or more) game where players take turns dropping checkers
to be the first to get 4 in a row horizontally, vertically, or diagonally.
"""

import os
import random

# Global constants
ROWS = 6
COLS = 7
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2
WINNING_LENGTH = 4


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * COLS + "+")


def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col


def is_column_full(board, col):
    """Check if a column is completely filled."""
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False if column is full.
    """
    if is_column_full(board, col):
        print("This column is full. Try another column.")
        return False
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a given direction.
    Returns the count of consecutive checkers in that direction.
    """
    count = 0
    r, c = row + row_delta, col + col_delta
    
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    return count


def check_win(board, row, col, checker):
    """
    Check if the last placed checker (at row, col) creates a winning condition.
    Returns True if there are 4 or more in a row, False otherwise.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]
    
    for row_delta, col_delta in directions:
        # Count in both directions
        count = 1  # Include the current checker
        
        # Count in positive direction
        count += check_direction(board, row, col, checker, row_delta, col_delta)
        
        # Count in negative direction
        count += check_direction(board, row, col, checker, -row_delta, -col_delta)
        
        if count >= WINNING_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely filled."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {checkers[current_player]} starts!\n")
    
    # Game loop
    while True:
        # Get valid column from current player
        while True:
            print(f"Player {checkers[current_player]}, please enter a column: ", end="")
            col = get_valid_column()
            
            if place_checker(board, col, checkers[current_player]):
                # Successfully placed checker
                # Find the row where checker was placed to check for win
                for row in range(ROWS):
                    if board[row][col] == checkers[current_player]:
                        placed_row = row
                        break
                
                print_board(board)
                
                # Check for win
                if check_win(board, placed_row, col, checkers[current_player]):
                    print(f"Player {checkers[current_player]} won!")
                    return
                
                # Check for draw
                if is_board_full(board):
                    print("It's a draw!")
                    return
                
                # Move to next player
                current_player = (current_player + 1) % NUM_PLAYERS
                break
            else:
                # Column was full, ask again (turn is not lost)
                continue


if __name__ == "__main__":
    play_game()
