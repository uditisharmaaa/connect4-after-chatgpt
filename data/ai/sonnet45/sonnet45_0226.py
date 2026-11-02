import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    """
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """
    Prints the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board rows with borders
    for row in range(ROWS):
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()

def is_valid_column(col_letter, board):
    """
    Validates if the column input is valid and not full.
    Returns (is_valid, col_index) tuple.
    """
    # Check if input is a single character
    if len(col_letter) != 1:
        return False, -1
    
    # Check if input is an uppercase letter
    if not col_letter.isupper() or not col_letter.isalpha():
        return False, -1
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False, -1
    
    # Check if column is not full (top row has space)
    if board[0][col_index] != " ":
        return False, -1
    
    return True, col_index

def place_checker(board, col_index, checker):
    """
    Places a checker in the specified column at the lowest available row.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from bottom row and work upwards
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """
    Checks if the last move at (row, col) resulted in a win.
    Checks horizontal, vertical, and both diagonal directions.
    """
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
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    if count >= 4:
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
    if count >= 4:
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
    if count >= 4:
        return True
    
    return False

def is_board_full(board):
    """
    Checks if the board is completely full (draw condition).
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = create_board()
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get valid column input from player
        valid_input = False
        while not valid_input:
            col_letter = input(f"Player {checker}, please enter a column: ")
            is_valid, col_index = is_valid_column(col_letter, board)
            
            if is_valid:
                valid_input = True
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Place the checker
        row = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
