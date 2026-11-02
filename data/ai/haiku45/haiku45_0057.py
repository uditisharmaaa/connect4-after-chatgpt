import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return an empty board with all spaces."""
    board = []
    for row in range(ROWS):
        board_row = []
        for col in range(COLS):
            board_row.append(" ")
        board.append(board_row)
    return board

def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print rows
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * COLS + "+")

def get_valid_column(current_player):
    """Get a valid column input from the current player."""
    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        
        # Check if input is a single letter
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - 65
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col

def place_checker(board, col, current_player):
    """Place a checker in the specified column. Return True if successful, False if column is full."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False

def check_win(board, row, col, current_player):
    """Check if the current player has won with their last move at (row, col)."""
    checker = CHECKERS[current_player]
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get valid column from player
        col = get_valid_column(current_player)
        
        # Try to place checker
        placed = False
        while not placed:
            placed = place_checker(board, col, current_player)
            if not placed:
                col = get_valid_column(current_player)
        
        # Find the row where the checker was placed
        placed_row = -1
        for row in range(ROWS):
            if board[row][col] == CHECKERS[current_player]:
                placed_row = row
                break
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, placed_row, col, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """Start the game."""
    play_game()

if __name__ == "__main__":
    main()
