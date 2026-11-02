import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board with specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print top border
    print("  " + "+---" * COLS + "+")
    
    # Print each row with borders
    for row in range(ROWS):
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
        print("  " + "+---" * COLS + "+")

def is_valid_column(column_input):
    """Check if the column input is a valid letter."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    if not column_input.isupper():
        return False
    col_index = ord(column_input) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return True

def is_column_full(board, col_index):
    """Check if the specified column is full."""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available row.
    Returns the row where the checker was placed, or -1 if column is full."""
    # Start from bottom row and go up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if placing a checker at (row, col) results in a win.
    Checks horizontal, vertical, and both diagonal directions."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    # Find the starting point of the diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    count = 0
    while start_row < ROWS and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1
    
    # Check diagonal (bottom-left to top-right)
    # Find the starting point of the diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    count = 0
    while start_row >= 0 and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    """Get and validate player move input."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(column_input) - 65
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get player move
        col_index = get_player_move(board, checker)
        
        # Place checker
        row = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Main entry point
if __name__ == "__main__":
    play_game()
