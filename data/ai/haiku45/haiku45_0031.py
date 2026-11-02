import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board in the required format."""
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(ord('A') + col)}   ", end="")
    print()
    
    # Print board rows with separators
    for row in range(rows):
        # Print separator line
        print("+---" * cols + "+")
        
        # Print board row
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom separator
    print("+---" * cols + "+")

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def get_player_input(cols):
    """Get valid column input from player."""
    while True:
        try:
            user_input = input("Please enter a column: ").strip().upper()
            
            # Validate input
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col_index = ord(user_input) - ord('A')
            
            if col_index < 0 or col_index >= cols:
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
                continue
            
            return col_index
            
        except Exception:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, player_symbol):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return True
    
    # Column is full
    return False

def check_win(board, row, col, player_symbol):
    """Check if the current move results in a win."""
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the current position
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_random_player(num_players):
    """Return a random starting player index."""
    return random.randint(0, num_players - 1)

def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Get player symbols
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Select random starting player
    current_player_index = get_random_player(NUM_PLAYERS)
    
    # Clear screen and print initial board
    clear_screen()
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column input
        while True:
            print(f"Player {current_player}, ", end="")
            col = get_player_input(BOARD_COLS)
            
            # Try to place checker
            if place_checker(board, col, current_player):
                last_row = None
                # Find the row where the checker was placed
                for row in range(BOARD_ROWS):
                    if board[row][col] == current_player:
                        last_row = row
                        break
                break
            else:
                print("Column is full. Please choose another column.")
        
        # Clear screen and print updated board
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, last_row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
