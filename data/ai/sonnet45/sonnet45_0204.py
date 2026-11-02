import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print rows with horizontal borders
    for row in range(ROWS):
        # Print top border of each cell
        print("  " + "+---" * COLS + "+")
        # Print cell contents
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  " + "+---" * COLS + "+")

def get_column_input(player_symbol):
    """Get and validate column input from player."""
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index

def place_checker(board, col, player_symbol):
    """
    Place a checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from the bottom row and work upward
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return row
    
    # Column is full
    return -1

def check_win(board, row, col, player_symbol):
    """
    Check if the last move at (row, col) resulted in a win.
    Returns True if player won, False otherwise.
    """
    # Check horizontal
    if check_direction(board, row, col, player_symbol, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, player_symbol, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, player_symbol, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, player_symbol, -1, 1):
        return True
    
    return False

def check_direction(board, row, col, player_symbol, delta_row, delta_col):
    """
    Check if there are WIN_LENGTH checkers in a row in a specific direction.
    """
    count = 1  # Count the current checker
    
    # Check in positive direction
    count += count_consecutive(board, row, col, player_symbol, delta_row, delta_col)
    
    # Check in negative direction
    count += count_consecutive(board, row, col, player_symbol, -delta_row, -delta_col)
    
    return count >= WIN_LENGTH

def count_consecutive(board, row, col, player_symbol, delta_row, delta_col):
    """
    Count consecutive checkers in one direction starting from (row, col).
    """
    count = 0
    current_row = row + delta_row
    current_col = col + delta_col
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == player_symbol):
        count += 1
        current_row += delta_row
        current_col += delta_col
    
    return count

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Set up players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column input
        while True:
            col = get_column_input(current_player)
            row = place_checker(board, col, current_player)
            
            if row == -1:
                print("Column is full. You lose your turn.")
                break
            
            # Valid move made
            print_board(board)
            
            # Check for win
            if check_win(board, row, col, current_player):
                print(f"Player {current_player} won!")
                return
            
            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                return
            
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
