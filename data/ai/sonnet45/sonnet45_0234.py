import random
import os

# Global constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

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
    
    # Print each row with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(column_input, board):
    """
    Validates if the column input is valid (exists and not full).
    Returns tuple: (is_valid, column_index, error_message)
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return False, -1, "Please enter a single letter."
    
    # Check if input is a letter
    if not column_input.isalpha():
        return False, -1, "Please enter a letter."
    
    # Convert to uppercase and get column index
    column_letter = column_input.upper()
    column_index = ord(column_letter) - 65
    
    # Check if column is within board range
    if column_index < 0 or column_index >= COLS:
        return False, -1, f"Column must be between A and {chr(64 + COLS)}."
    
    # Check if column is not full
    if board[0][column_index] != " ":
        return False, -1, "This column is full. Please choose another column."
    
    return True, column_index, ""

def place_checker(board, column_index, checker):
    """
    Places a checker in the specified column at the lowest available row.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from the bottom row and move up
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """
    Checks if the last move resulted in a win.
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
    Main game loop that controls the Connect 4 game.
    """
    # Initialize the board
    board = create_board()
    
    # Get player checkers based on number of players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid input from current player
        valid_input = False
        while not valid_input:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            is_valid, column_index, error_message = is_valid_column(column_input, board)
            
            if is_valid:
                valid_input = True
            else:
                print(error_message)
        
        # Place the checker
        row = place_checker(board, column_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, column_index, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
