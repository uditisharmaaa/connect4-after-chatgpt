import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    Board is a list of lists where board[row][col] represents a cell.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print top border of row
        print("  " + "+---" * COLS + "+")
        # Print row content
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  " + "+---" * COLS + "+")


def get_valid_input(player_symbol):
    """
    Prompts the player for input and validates it.
    Returns the column index (0-based) if valid.
    Continues asking until valid input is received.
    """
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_symbol):
    """
    Places a checker in the specified column.
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
    Checks if placing a checker at (row, col) creates a winning condition.
    Checks horizontal, vertical, and both diagonal directions.
    Returns True if player wins, False otherwise.
    """
    # Check horizontal
    if check_direction(board, row, col, player_symbol, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, player_symbol, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, player_symbol, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, player_symbol, -1, 1):
        return True
    
    return False


def check_direction(board, row, col, player_symbol, delta_row, delta_col):
    """
    Checks if there are 4 consecutive checkers in a specific direction.
    delta_row and delta_col define the direction to check.
    """
    count = 1  # Count the current checker
    
    # Check in positive direction
    count += count_consecutive(board, row, col, player_symbol, delta_row, delta_col)
    
    # Check in negative direction
    count += count_consecutive(board, row, col, player_symbol, -delta_row, -delta_col)
    
    return count >= WIN_LENGTH


def count_consecutive(board, row, col, player_symbol, delta_row, delta_col):
    """
    Counts consecutive checkers of the same player in a given direction.
    """
    count = 0
    current_row = row + delta_row
    current_col = col + delta_col
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == player_symbol):
        count += 1
        current_row += delta_row
        current_col += delta_col
    
    return count


def is_board_full(board):
    """
    Checks if the board is completely full (draw condition).
    Returns True if board is full, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop that handles the Connect 4 game flow.
    """
    # Initialize board
    board = create_board()
    
    # Get player symbols based on number of players
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column from player
        col = get_valid_input(current_player)
        
        # Place checker
        row = place_checker(board, col, current_player)
        
        # Check if column was full
        if row == -1:
            print("Column is full! You lose your turn.")
            print_board(board)
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


# Start the game
if __name__ == "__main__":
    play_game()
