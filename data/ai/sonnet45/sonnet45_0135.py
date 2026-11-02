import random
import os

# Global constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board with dimensions NUM_ROWS x NUM_COLS."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(NUM_COLS):
        print(chr(65 + i), end="   ")
    print()
    
    # Print board rows with borders
    for row in board:
        print("+" + "---+" * NUM_COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * NUM_COLS)

def is_valid_column(col_letter, board):
    """
    Check if the column input is valid.
    Returns (is_valid, col_index) tuple.
    """
    # Check if input is a single character
    if len(col_letter) != 1:
        return False, -1
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False, -1
    
    # Convert letter to column index
    col_index = ord(col_letter) - ord('A')
    
    # Check if column is within board range
    if col_index < 0 or col_index >= NUM_COLS:
        return False, -1
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False, -1
    
    return True, col_index

def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    Returns the row index where the checker was placed, or -1 if column is full.
    """
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """
    Check if the last move at (row, col) resulted in a win.
    Returns True if the player won, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < NUM_ROWS and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(NUM_ROWS - 1 - row, col)
    start_col = col - min(NUM_ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {checker}, please enter a column: ")
            is_valid, col_index = is_valid_column(col_input, board)
            
            if is_valid:
                valid_input = True
            else:
                print("Invalid input. Please try again.")
        
        # Place checker
        row_placed = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_placed, col_index, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
