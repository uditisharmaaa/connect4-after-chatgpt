import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def create_board():
    """Create and return an empty board with the specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_input(user_input, board):
    """Check if the user input is valid."""
    # Check if input is a single character
    if len(user_input) != 1:
        return False
    
    # Check if input is a letter
    if not user_input.isalpha():
        return False
    
    # Convert to uppercase and check if within board range
    col_letter = user_input.upper()
    col_index = ord(col_letter) - ord('A')
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space
    if board[0][col_index] != " ":
        return False
    
    return True

def get_column_input(player_checker, board):
    """Get and validate column input from the player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        if is_valid_input(user_input, board):
            return ord(user_input.upper()) - ord('A')
        else:
            print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

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
    if check_direction(board, row, col, checker, 1, -1):
        return True
    
    return False

def check_direction(board, row, col, checker, row_dir, col_dir):
    """Check if there are 4 checkers in a row in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    count += count_in_direction(board, row, col, checker, row_dir, col_dir)
    
    # Check in negative direction
    count += count_in_direction(board, row, col, checker, -row_dir, -col_dir)
    
    return count >= WIN_LENGTH

def count_in_direction(board, row, col, checker, row_dir, col_dir):
    """Count consecutive checkers in a specific direction."""
    count = 0
    r = row + row_dir
    c = col + col_dir
    
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += row_dir
        c += col_dir
    
    return count

def is_board_full(board):
    """Check if the board is completely full."""
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
        checker = CHECKERS[current_player]
        
        # Get valid column input
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
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
