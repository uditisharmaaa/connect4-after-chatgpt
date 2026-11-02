import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Create and return a board with all cells initialized to spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()

def get_valid_input(cols):
    """Get and validate player input for column choice."""
    while True:
        user_input = input("Enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Column is out of board range.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False

def check_winner(board, row, col, checker):
    """Check if the last placed checker at (row, col) creates a win."""
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal right, diagonal left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the checker we just placed
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        # If we have 4 or more in a row, it's a win
        if count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_last_row(board, col):
    """Get the row index where the last checker was placed in a column."""
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] != " ":
            return row
    return -1

def play_game():
    """Main game loop."""
    os.system('clear')
    
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Print initial board
    print_board(board)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player]
    
    # Game loop
    while True:
        # Print current player
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column input
        col = get_valid_input(COLS)
        
        # Try to place checker
        if place_checker(board, col, current_checker):
            # Get the row where checker was placed
            row = get_last_row(board, col)
            
            # Clear screen and print updated board
            os.system('clear')
            print_board(board)
            
            # Check for winner
            if check_winner(board, row, col, current_checker):
                print(f"Player {current_checker} won!")
                break
            
            # Check for draw
            if is_board_full(board):
                print("It's a draw!")
                break
            
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player]
        else:
            # Column was full, player loses turn
            print("Column is full. You lose your turn.")
            print()
            
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player]
            
            os.system('clear')
            print_board(board)

# Run the game
if __name__ == "__main__":
    play_game()
