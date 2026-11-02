import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Create and return a 2D board initialized with empty spaces.
    Board is a list of rows, where each row is a list of columns.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board


def print_board(board):
    """
    Print the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        
        # Print border after each row
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()


def is_valid_column(column_input, board):
    """
    Check if the column input is valid.
    Returns (valid, column_index) tuple.
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return False, -1
    
    # Check if input is an uppercase letter
    if not column_input.isupper():
        return False, -1
    
    # Convert letter to column index
    col_index = ord(column_input) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False, -1
    
    # Check if column has space (top row not filled)
    if board[0][col_index] != " ":
        return False, -1
    
    return True, col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column at the lowest available row.
    Returns the row where the checker was placed.
    """
    # Start from bottom row and work upwards
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """
    Check if placing a checker at (row, col) creates a winning condition.
    Checks horizontal, vertical, and both diagonal directions.
    """
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    count = 0
    while start_row < ROWS and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1
    
    # Check diagonal (bottom-left to top-right)
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    count = 0
    while start_row >= 0 and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled (draw condition).
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop that handles the Connect 4 game.
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
        
        # Prompt player for input
        column_input = input(f"Player {checker}, please enter a column: ")
        
        # Validate input
        valid, col_index = is_valid_column(column_input, board)
        
        if not valid:
            # Invalid input - ask again without losing turn
            print_board(board)
            print("Invalid input! Please try again.")
            continue
        
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


# Start the game
if __name__ == "__main__":
    play_game()
