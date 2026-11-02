import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board with the specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """Check if the column input is valid and not full."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full (top row has space)
    if board[0][col_index] != " ":
        return False
    
    return True

def get_column_input(player_checker, board):
    """Get and validate column input from the player."""
    while True:
        col_letter = input(f"Player {player_checker}, please enter a column: ")
        
        if is_valid_column(col_letter, board):
            return ord(col_letter) - 65
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, checker):
    """Place a checker in the specified column at the lowest available row."""
    # Start from bottom row and find the first empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full (shouldn't happen if validated)

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, checker, -1, 1):
        return True
    
    return False

def check_direction(board, row, col, checker, row_dir, col_dir):
    """Check if there are 4 checkers in a row in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in the positive direction
    count += count_checkers(board, row, col, checker, row_dir, col_dir)
    
    # Check in the negative direction
    count += count_checkers(board, row, col, checker, -row_dir, -col_dir)
    
    return count >= 4

def count_checkers(board, row, col, checker, row_dir, col_dir):
    """Count consecutive checkers in a given direction."""
    count = 0
    r = row + row_dir
    c = col + col_dir
    
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += row_dir
        c += col_dir
    
    return count

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get column input from player
        col = get_column_input(checker, board)
        
        # Place the checker
        row = place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
