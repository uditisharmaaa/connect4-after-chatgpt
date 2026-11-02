import random
import os

# ============================================================================
# CONSTANTS - Modify these to change game settings
# ============================================================================
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5 players
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player symbols

# ============================================================================
# GAME BOARD FUNCTIONS
# ============================================================================

def create_board():
    """
    Creates and returns an empty game board.
    Board is a 2D list with ROWS rows and COLS columns, filled with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board


def print_board(board):
    """
    Prints the current game board with column labels (A-G) and row numbers.
    Clears the screen first for a clean display.
    """
    os.system('clear')
    
    # Print column labels
    print("\n  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")  # 65 is ASCII for 'A'
    print()
    
    # Print top border
    print("  " + "----" * COLS)
    
    # Print each row with row number
    for row in range(ROWS):
        print(f"{row + 1} ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
        print("  " + "----" * COLS)
    print()


def drop_piece(board, col, player):
    """
    Drops a piece for the given player into the specified column.
    Returns True if successful, False if column is full.
    Pieces fall to the lowest available row in the column.
    """
    # Start from the bottom row and work up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False  # Column is full


# ============================================================================
# INPUT VALIDATION
# ============================================================================

def get_valid_move(board, player):
    """
    Prompts the current player for a column choice and validates it.
    Returns the column index (0-6) once a valid move is entered.
    """
    while True:
        move = input(f"Player {player}, enter column (A-G): ").upper().strip()
        
        # Check if input is a single character
        if len(move) != 1:
            print("Please enter a single letter from A to G.")
            continue
        
        # Check if input is a letter A-G
        if move < 'A' or move > chr(65 + COLS - 1):
            print(f"Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        
        # Convert letter to column index (A=0, B=1, etc.)
        col = ord(move) - 65
        
        # Check if column has space
        if board[0][col] != ' ':
            print("That column is full! Try another column.")
            continue
        
        return col


# ============================================================================
# WIN CHECKING
# ============================================================================

def check_win(board, player):
    """
    Checks if the specified player has won the game.
    Returns True if player has 4 in a row (horizontal, vertical, or diagonal).
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row][col + 1] == player and
                board[row][col + 2] == player and
                board[row][col + 3] == player):
                return True
    
    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and
                board[row + 1][col] == player and
                board[row + 2][col] == player and
                board[row + 3][col] == player):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row - 1][col + 1] == player and
                board[row - 2][col + 2] == player and
                board[row - 3][col + 3] == player):
                return True
    
    return False


def check_draw(board):
    """
    Checks if the game is a draw (board is full with no winner).
    Returns True if the top row is completely filled.
    """
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


# ============================================================================
# MAIN GAME FUNCTION
# ============================================================================

def play_game():
    """
    Main game loop that runs the Connect 4 game.
    Handles player turns, move validation, win checking, and game flow.
    """
    # Initialize the game
    board = create_board()
    
    # Get the player symbols based on NUM_PLAYERS
    active_players = PLAYERS[:NUM_PLAYERS]
    
    # Randomly select which player goes first
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("=" * 40)
    print("       WELCOME TO CONNECT 4!")
    print("=" * 40)
    print(f"\nNumber of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(active_players)}")
    print(f"\nPlayer {active_players[current_player_index]} will go first!")
    input("\nPress Enter to start...")
    
    # Main game loop
    while True:
        # Get current player symbol
        current_player = active_players[current_player_index]
        
        # Display the board
        print_board(board)
        
        # Get and execute player's move
        col = get_valid_move(board, current_player)
        drop_piece(board, col, current_player)
        
        # Check if current player won
        if check_win(board, current_player):
            print_board(board)
            print("=" * 40)
            print(f"   Player {current_player} WINS!")
            print("=" * 40)
            break
        
        # Check if game is a draw
        if check_draw(board):
            print_board(board)
            print("=" * 40)
            print("   DRAW! The board is full!")
            print("=" * 40)
            break
        
        # Move to next player (rotate through all players)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    play_game()
    
    # Ask if players want to play again
    while True:
        again = input("\nPlay again? (y/n): ").lower().strip()
        if again == 'y':
            play_game()
        elif again == 'n':
            print("\nThanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'.")
