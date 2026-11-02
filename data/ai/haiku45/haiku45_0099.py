"""
Connect 4 Game Implementation
A two-player game where players take turns dropping checkers into columns.
The first player to get 4 checkers in a row (horizontally, vertically, or diagonally) wins.
"""

import os
import random

# Game configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and return an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col):3}", end=" ")
    print()
    
    # Print board with row separators
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_column_valid(board, col, cols):
    """Check if the column index is valid and not full."""
    if col < 0 or col >= cols:
        return False
    if board[0][col] != " ":
        return False
    return True


def get_valid_column_input(cols):
    """Get and validate player's column input."""
    while True:
        user_input = input("Please enter a column (A-{}): ".format(chr(65 + cols - 1))).strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if user_input < 'A' or user_input >= chr(65 + cols):
            print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        col = ord(user_input) - ord('A')
        return col


def place_checker(board, col, checker, rows):
    """Place a checker in the specified column and return the row where it was placed."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full


def check_horizontal_win(board, row, col, checker, cols):
    """Check if there's a winning sequence horizontally."""
    count = 0
    
    # Count consecutive checkers to the left
    c = col
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Count consecutive checkers to the right (excluding the current cell)
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker, rows):
    """Check if there's a winning sequence vertically."""
    count = 0
    
    # Count consecutive checkers downward
    r = row
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    
    # Count consecutive checkers upward (excluding the current cell)
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, checker, rows, cols):
    """Check if there's a winning sequence diagonally (both directions)."""
    # Check diagonal from top-left to bottom-right
    count = 0
    r, c = row, col
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 0
    r, c = row, col
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def check_win(board, row, col, checker, rows, cols):
    """Check if the current move results in a win."""
    if check_horizontal_win(board, row, col, checker, cols):
        return True
    if check_vertical_win(board, row, col, checker, rows):
        return True
    if check_diagonal_win(board, row, col, checker, rows, cols):
        return True
    return False


def check_draw(board, rows, cols):
    """Check if the board is full (draw condition)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize the game
    board = initialize_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player]
    
    # Print initial board
    print_board(board, COLS)
    print(f"Game started with {NUM_PLAYERS} player(s).")
    print(f"Player {current_checker} starts first.\n")
    
    # Game loop
    game_over = False
    while not game_over:
        # Get player input
        print(f"Player {current_checker}, please enter a column:")
        col = get_valid_column_input(COLS)
        
        # Check if column is full
        if not is_column_valid(board, col, COLS):
            print("Column is full. Please choose another column.\n")
            continue
        
        # Place the checker
        row = place_checker(board, col, current_checker, ROWS)
        
        # Print updated board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, row, col, current_checker, ROWS, COLS):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board, ROWS, COLS):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player]


if __name__ == "__main__":
    play_game()
