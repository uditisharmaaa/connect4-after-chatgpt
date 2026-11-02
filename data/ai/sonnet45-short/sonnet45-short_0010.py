import random
import os

# Constants for game configuration
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Available player symbols

# Initialize the game board as a 2D list filled with spaces
def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Display the current state of the board
def print_board(board):
    """Print the game board with column labels and row numbers."""
    os.system('clear')  # Clear the screen
    
    # Print column labels (A-G)
    print('  ', end='')
    for i in range(NUM_COLS):
        print(chr(65 + i), end=' ')  # Convert 0-6 to A-G
    print()
    
    # Print top border
    print(' +' + '-' * (NUM_COLS * 2 - 1) + '+')
    
    # Print each row with its contents
    for row in range(NUM_ROWS):
        print(str(row) + '|', end='')
        for col in range(NUM_COLS):
            print(board[row][col] + '|', end='')
        print()
    
    # Print bottom border
    print(' +' + '-' * (NUM_COLS * 2 - 1) + '+')

# Get valid column input from the player
def get_column_input(player):
    """Prompt player for column choice and validate input."""
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper().strip()
        
        # Check if input is a single character
        if len(choice) != 1:
            print("Please enter a single letter.")
            continue
        
        # Check if input is a valid column letter
        if choice < 'A' or choice > chr(65 + NUM_COLS - 1):
            print(f"Please enter a letter between A and {chr(65 + NUM_COLS - 1)}.")
            continue
        
        # Convert letter to column index (A=0, B=1, etc.)
        return ord(choice) - 65

# Drop a piece into the specified column
def drop_piece(board, col, player):
    """
    Drop a piece into the given column for the current player.
    Returns the row where the piece landed, or -1 if column is full.
    """
    # Start from the bottom row and work upward
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    
    # Column is full
    return -1

# Check if there are four in a row starting from a given position
def check_line(board, row, col, delta_row, delta_col, player):
    """
    Check if there are 4 consecutive pieces in a line.
    delta_row and delta_col define the direction to check.
    """
    count = 0
    
    # Check up to 4 positions in the given direction
    for i in range(4):
        r = row + i * delta_row
        c = col + i * delta_col
        
        # Check if position is within bounds and contains player's symbol
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player:
            count += 1
        else:
            break
    
    return count == 4

# Check if the current player has won
def check_win(board, row, col, player):
    """
    Check if the last move resulted in a win.
    Checks horizontal, vertical, and both diagonal directions.
    """
    # Check horizontal (left and right from the piece)
    for start_col in range(max(0, col - 3), min(NUM_COLS - 3, col + 1)):
        if check_line(board, row, start_col, 0, 1, player):
            return True
    
    # Check vertical (downward from the piece)
    if check_line(board, row, col, 1, 0, player):
        return True
    
    # Check diagonal (down-right)
    for offset in range(-3, 1):
        start_row = row + offset
        start_col = col + offset
        if check_line(board, start_row, start_col, 1, 1, player):
            return True
    
    # Check diagonal (down-left)
    for offset in range(-3, 1):
        start_row = row + offset
        start_col = col - offset
        if check_line(board, start_row, start_col, 1, -1, player):
            return True
    
    return False

# Check if the board is completely full (draw condition)
def check_draw(board):
    """Check if the board is full (no more moves possible)."""
    # Check if the top row has any empty spaces
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

# Main game loop
def play_game():
    """Main function to run the Connect 4 game."""
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]  # Get the first N player symbols
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Random starting player
    
    print(f"Welcome to Connect 4!")
    print(f"Number of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Display the board
        print_board(board)
        
        # Get player input
        col = get_column_input(current_player)
        
        # Attempt to drop the piece
        row = drop_piece(board, col, current_player)
        
        # Check if column was full
        if row == -1:
            print("That column is full! Try another column.")
            input("Press Enter to continue...")
            continue
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
