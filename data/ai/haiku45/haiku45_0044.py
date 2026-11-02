import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, columns):
    """Initialize an empty board with all whitespaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    columns = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+---" * columns + "+")
        
        # Row content
        print("|", end="")
        for col in range(columns):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Bottom border
    print("+---" * columns + "+")


def get_column_input(columns):
    """Get valid column input from user."""
    while True:
        user_input = input().upper().strip()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= columns:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    
    return False


def check_win(board, row, col, checker):
    """Check if the last placed checker at (row, col) results in a win."""
    rows = len(board)
    columns = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (\), diagonal (/)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1)   # diagonal /
    ]
    
    for dx, dy in directions:
        count = 1  # Count the checker itself
        
        # Check in positive direction
        x, y = row + dx, col + dy
        while 0 <= x < rows and 0 <= y < columns and board[x][y] == checker:
            count += 1
            x += dx
            y += dy
        
        # Check in negative direction
        x, y = row - dx, col - dy
        while 0 <= x < rows and 0 <= y < columns and board[x][y] == checker:
            count += 1
            x -= dx
            y -= dy
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    checkers = CHECKERS[:NUM_PLAYERS]
    
    # Choose random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    winner = None
    
    # Main game loop
    while not game_over:
        current_checker = checkers[current_player_index]
        current_player_name = chr(ord('A') + current_player_index) if current_player_index > 0 else current_checker
        
        print(f"Player {current_checker}, please enter a column:")
        col = get_column_input(COLUMNS)
        
        # Try to place checker
        if not place_checker(board, col, current_checker):
            print("Column is full. Please choose another column.")
            continue
        
        # Get the row where checker was placed
        placed_row = -1
        for row in range(ROWS):
            if board[row][col] == current_checker:
                placed_row = row
                break
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, placed_row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
            winner = current_checker
        
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
