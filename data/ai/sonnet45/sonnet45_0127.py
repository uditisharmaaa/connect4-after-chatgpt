import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(NUM_COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board rows with borders
    for row in range(NUM_ROWS):
        # Print top border
        print("+", end="")
        for col in range(NUM_COLS):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(NUM_COLS):
        print("---+", end="")
    print()

def get_valid_input(player_checker, board):
    """Get and validate user input for column selection."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is an uppercase letter
        if not user_input.isupper() or not user_input.isalpha():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within board range
        if col_index < 0 or col_index >= NUM_COLS:
            print(f"Invalid column. Please choose between A and {chr(64 + NUM_COLS)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn.")
            return -1
        
        return col_index

def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available position."""
    # Find the lowest empty row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    
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
    
    # Check diagonal (top-left to bottom-right)
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    count = 0
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
    
    # Check diagonal (bottom-left to top-right)
    start_row = row + min(NUM_ROWS - 1 - row, col)
    start_col = col - min(NUM_ROWS - 1 - row, col)
    count = 0
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

def check_draw(board):
    """Check if the board is full (draw condition)."""
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
    while True:
        player_checker = CHECKERS[current_player]
        
        # Get valid column input
        col_index = get_valid_input(player_checker, board)
        
        # If column was full, skip to next player
        if col_index == -1:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        row_index = place_checker(board, col_index, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
