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
    Creates and returns a 2D list representing the game board.
    All cells are initialized with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    """
    Prints the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """
    Validates if the column input is valid.
    Returns the column index if valid, -1 otherwise.
    """
    # Check if input is a single character
    if len(col_letter) != 1:
        return -1
    
    # Check if it's an uppercase letter
    if not col_letter.isupper():
        return -1
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return -1
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return -1
    
    return col_index

def place_checker(board, col_index, checker):
    """
    Places a checker in the specified column at the lowest available row.
    Returns the row index where the checker was placed.
    """
    # Start from bottom row and go up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """
    Checks if the last move resulted in a win.
    Checks horizontal, vertical, and both diagonal directions.
    """
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
    count = 0
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    # Check along diagonal
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
    count = 0
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    # Check along diagonal
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

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
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
        
        # Get player input
        valid_move = False
        while not valid_move:
            col_input = input(f"Player {checker}, please enter a column: ")
            col_index = is_valid_column(col_input, board)
            
            if col_index == -1:
                print("Invalid input. Please enter a valid column letter.")
            else:
                valid_move = True
        
        # Place checker
        row_placed = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_placed, col_index, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
