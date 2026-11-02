import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board with specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the game board with column labels."""
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
    
    # Print bottom border
    print("+" + "---+" * COLS)


def get_column_input(player_symbol):
    """Get and return valid column input from player."""
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is an uppercase letter
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLS)}.")
            continue
        
        return col_index


def place_checker(board, col, player_symbol):
    """
    Place a checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from bottom row and find first empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return row
    
    # Column is full
    return -1


def check_win(board, row, col, player_symbol):
    """
    Check if placing a checker at (row, col) results in a win.
    Returns True if player wins, False otherwise.
    """
    # Define direction vectors: (row_delta, col_delta)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        
        # Check if we have WIN_LENGTH in a row
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select players
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column input
        col = get_column_input(current_player)
        
        # Place checker
        row = place_checker(board, col, current_player)
        
        # Check if column was full
        if row == -1:
            print_board(board)
            print("Column is full! You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
