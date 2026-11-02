import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print top border
    print("  " + "+---" * COLS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
        print("  " + "+---" * COLS + "+")

def is_valid_input(column_input):
    """Check if the input is a single uppercase letter."""
    return len(column_input) == 1 and column_input.isalpha() and column_input.isupper()

def get_column_index(column_input):
    """Convert column letter to index (A->0, B->1, etc.)."""
    return ord(column_input) - 65

def is_column_in_range(col_index):
    """Check if the column index is within the board range."""
    return 0 <= col_index < COLS

def is_column_full(board, col_index):
    """Check if a column is completely filled."""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available row."""
    # Start from the bottom row and find the first empty cell
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    
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
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find the starting position of the diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    # Check along the diagonal
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find the starting position of the diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    # Check along the diagonal
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely filled (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    """Get and validate player input for their move."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Validate input format
        if not is_valid_input(column_input):
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        
        # Convert to column index
        col_index = get_column_index(column_input)
        
        # Check if column is in range
        if not is_column_in_range(col_index):
            print("Column out of range. Please enter a valid column letter.")
            continue
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
            return -1
        
        return col_index

def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        player_checker = CHECKERS[current_player]
        
        # Get player move
        col_index = get_player_move(board, player_checker)
        
        # If column was full, skip turn
        if col_index == -1:
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        # Place the checker
        row = place_checker(board, col_index, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, player_checker):
            print(f"Player {player_checker} won!")
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
