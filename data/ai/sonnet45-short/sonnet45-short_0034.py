import random
import os

# ============================================================================
# CONSTANTS - Modify these to change game settings
# ============================================================================
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 for different number of players
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Take first N players

# ============================================================================
# GAME BOARD FUNCTIONS
# ============================================================================

def create_board():
    """
    Creates and returns an empty game board as a 2D list.
    Each cell is initialized with a space character ' '.
    """
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """
    Displays the current game board to the console.
    Shows column labels (A-G) at the top and the grid below.
    """
    os.system('clear')  # Clear the screen for a clean display
    
    # Print column labels
    print('\n  ', end='')
    for i in range(COLS):
        print(chr(65 + i), end=' ')  # Convert 0-6 to A-G using ASCII
    print('\n  ' + '-' * (COLS * 2 - 1))
    
    # Print each row with row numbers
    for row in range(ROWS):
        print(f'{row + 1}|', end='')
        for col in range(COLS):
            print(board[row][col] + '|', end='')
        print()
    
    print('  ' + '-' * (COLS * 2 - 1))
    print()


# ============================================================================
# INPUT VALIDATION
# ============================================================================

def get_valid_column(board, player):
    """
    Prompts the player for a column choice and validates it.
    Returns the column index (0-6) when valid input is received.
    Validates that:
    - Input is a single character
    - Input is a letter A-G
    - The chosen column is not full
    """
    while True:
        choice = input(f"Player {player}'s turn. Choose column (A-G): ").strip().upper()
        
        # Check if input is a single character
        if len(choice) != 1:
            print("Please enter a single letter!")
            continue
        
        # Check if input is between A and G
        if choice < 'A' or choice > chr(65 + COLS - 1):
            print(f"Please enter a letter between A and {chr(65 + COLS - 1)}!")
            continue
        
        col = ord(choice) - 65  # Convert letter to column index (A=0, B=1, etc.)
        
        # Check if column has space (top row must be empty)
        if board[0][col] != ' ':
            print("That column is full! Choose another.")
            continue
        
        return col


# ============================================================================
# GAME LOGIC
# ============================================================================

def drop_piece(board, col, player):
    """
    Drops a player's piece into the specified column.
    The piece falls to the lowest available row in that column.
    Returns the row where the piece landed.
    """
    # Start from the bottom row and move up to find empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Should never happen if input validation works


def check_win(board, row, col, player):
    """
    Checks if the last move at (row, col) created a winning condition.
    Checks all four directions: horizontal, vertical, and both diagonals.
    Returns True if the player has 4 in a row, False otherwise.
    """
    
    def count_direction(delta_row, delta_col):
        """
        Helper function to count consecutive pieces in one direction.
        delta_row and delta_col specify the direction to check.
        """
        count = 0
        r, c = row + delta_row, col + delta_col
        
        # Keep counting while we're in bounds and find matching pieces
        while (0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player):
            count += 1
            r += delta_row
            c += delta_col
        
        return count
    
    # Check horizontal (left + right + center piece)
    horizontal = count_direction(0, -1) + count_direction(0, 1) + 1
    
    # Check vertical (only need to check downward + center piece)
    vertical = count_direction(1, 0) + 1
    
    # Check diagonal (bottom-left to top-right)
    diagonal1 = count_direction(1, -1) + count_direction(-1, 1) + 1
    
    # Check diagonal (top-left to bottom-right)
    diagonal2 = count_direction(-1, -1) + count_direction(1, 1) + 1
    
    # Win if any direction has 4 or more in a row
    return horizontal >= 4 or vertical >= 4 or diagonal1 >= 4 or diagonal2 >= 4


def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if the top row is completely filled, False otherwise.
    """
    return all(board[0][col] != ' ' for col in range(COLS))


# ============================================================================
# MAIN GAME LOOP
# ============================================================================

def play_game():
    """
    Main function that runs the Connect 4 game.
    Handles the game loop, turn management, and game end conditions.
    """
    # Initialize the game
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Random first player
    
    print("=" * 40)
    print("       WELCOME TO CONNECT 4!")
    print("=" * 40)
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"First player: {PLAYERS[current_player_index]}")
    input("\nPress Enter to start...")
    
    # Main game loop
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        # Get valid column choice from current player
        col = get_valid_column(board, current_player)
        
        # Drop the piece and get the row where it landed
        row = drop_piece(board, col, current_player)
        
        # Check if this move wins the game
        if check_win(board, row, col, current_player):
            print_board(board)
            print("=" * 40)
            print(f"   🎉 PLAYER {current_player} WINS! 🎉")
            print("=" * 40)
            break
        
        # Check if the board is full (draw)
        if check_draw(board):
            print_board(board)
            print("=" * 40)
            print("      IT'S A DRAW!")
            print("=" * 40)
            break
        
        # Move to next player (cycle through all players)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    play_game()
