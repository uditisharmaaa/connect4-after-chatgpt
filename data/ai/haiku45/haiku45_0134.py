import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board with all cells containing whitespace."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board


def print_board(board):
    """Clear screen and print the current board state."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with rows
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")


def get_column_input(board, current_player_checker):
    """Get valid column input from the player."""
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Validate input is a single letter
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Validate column is within board bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a column between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column and return the row it was placed in."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full


def check_win(board, row, col, checker):
    """Check if the player has won after placing a checker at (row, col)."""
    # Directions: horizontal, vertical, diagonal right, diagonal left
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal right
        (1, -1)   # Diagonal left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the checker we just placed
        
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
        
        # If we have 4 or more in a row, we have a win
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def get_current_checker(current_player):
    """Return the checker for the current player."""
    return CHECKERS[current_player]


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = get_current_checker(current_player)
        
        # Get valid column input from current player
        col = get_column_input(board, current_checker)
        
        # Place checker and get row
        row = place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
