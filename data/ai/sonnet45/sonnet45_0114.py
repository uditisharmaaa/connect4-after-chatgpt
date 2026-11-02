import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    Board has ROWS rows and COLS columns.
    """
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    """
    Prints the current state of the board with column labels.
    Columns are labeled A, B, C, etc.
    """
    # Clear screen before printing
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i), end="   ")
    print()
    
    # Print board rows with borders
    for row in range(ROWS):
        # Print top border of row
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()

def get_valid_input(player_checker):
    """
    Gets and validates user input for column selection.
    Returns the column index (0-based) if valid.
    Keeps asking until valid input is provided.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is an uppercase letter
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board boundaries
        if col_index < 0 or col_index >= COLS:
            print("Invalid input. Column out of range.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """
    Places a checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from bottom row and find first empty cell
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    
    # Column is full
    return -1

def check_win(board, row, col, checker):
    """
    Checks if placing a checker at (row, col) results in a win.
    Checks horizontal, vertical, and diagonal directions.
    Returns True if there are 4 in a row, False otherwise.
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
    # Find starting point of diagonal
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
    # Find starting point of diagonal
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

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if board is full, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get valid column input from player
        col = get_valid_input(checker)
        
        # Place checker in the column
        row = place_checker(board, col, checker)
        
        # Check if column was full
        if row == -1:
            print("Column is full. You lose your turn.")
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
