import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board with dimensions ROWS x COLS."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board rows with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_column(column_input, board):
    """Check if the column input is valid and has space available."""
    # Check if input is a single character
    if len(column_input) != 1:
        return False, "Invalid input. Please enter a single column letter."
    
    # Check if input is a letter
    if not column_input.isalpha():
        return False, "Invalid input. Please enter a letter."
    
    # Convert to column index
    col_index = ord(column_input.upper()) - ord('A')
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False, f"Column out of range. Please enter a letter between A and {chr(65 + COLS - 1)}."
    
    # Check if column has space available (top row not full)
    if board[0][col_index] != " ":
        return False, "Column is full. Please choose another column."
    
    return True, col_index


def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available row."""
    # Start from bottom row and move up to find the first empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
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
    if check_direction(board, row, col, checker, -1, 1):
        return True
    
    return False


def check_direction(board, row, col, checker, row_dir, col_dir):
    """Check if there are 4 checkers in a row in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + row_dir, col + col_dir
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += row_dir
        c += col_dir
    
    # Check in negative direction
    r, c = row - row_dir, col - col_dir
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r -= row_dir
        c -= col_dir
    
    return count >= WIN_LENGTH


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
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
        checker = CHECKERS[current_player]
        
        # Get valid input from current player
        while True:
            column_input = input(f"Player {checker}, please enter a column: ")
            is_valid, result = is_valid_column(column_input, board)
            
            if is_valid:
                col_index = result
                break
            else:
                print(result)
        
        # Place the checker
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


if __name__ == "__main__":
    play_game()
