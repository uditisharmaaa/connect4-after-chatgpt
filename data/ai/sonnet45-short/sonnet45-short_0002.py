import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create and return an empty game board."""
    # Create a 2D list filled with empty spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the current state of the board."""
    # Clear the screen for a clean display
    os.system('clear')
    
    # Print column labels
    print('\n  ' + '   '.join(COLUMN_LABELS))
    print(' ' + '---' * COLS + '--')
    
    # Print each row with its contents
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print(' ' + '---' * COLS + '--')
    print()

def drop_piece(board, col, token):
    """
    Drop a token into the specified column.
    Returns True if successful, False if column is full.
    """
    # Start from the bottom row and work upward
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return True
    # Column is full
    return False

def check_win(board, token):
    """
    Check if the specified token has won the game.
    Checks horizontal, vertical, and diagonal connections.
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == token and
                board[row][col + 1] == token and
                board[row][col + 2] == token and
                board[row][col + 3] == token):
                return True
    
    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == token and
                board[row + 1][col] == token and
                board[row + 2][col] == token and
                board[row + 3][col] == token):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == token and
                board[row - 1][col + 1] == token and
                board[row - 2][col + 2] == token and
                board[row - 3][col + 3] == token):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == token and
                board[row + 1][col + 1] == token and
                board[row + 2][col + 2] == token and
                board[row + 3][col + 3] == token):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    # If any space in the top row is empty, game can continue
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_input():
    """
    Get and validate the column choice from the player.
    Returns the column index (0-6).
    """
    while True:
        choice = input(f"Choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").upper()
        
        # Check if input is a valid column label
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        else:
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")

def get_number_of_players():
    """Get and validate the number of players for the game."""
    while True:
        try:
            num_players = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            
            # Check if number is within valid range
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                return num_players
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def play_game():
    """Main game loop."""
    # Setup phase
    print("Welcome to Connect 4!")
    print("=" * 40)
    
    # Get number of players and set up their tokens
    num_players = get_number_of_players()
    players = PLAYER_TOKENS[:num_players]
    
    # Create the game board
    board = create_board()
    
    # Randomly select which player goes first
    current_player_index = random.randint(0, num_players - 1)
    print(f"\nPlayer {players[current_player_index]} will go first!")
    input("Press Enter to start the game...")
    
    # Game loop
    while True:
        # Get current player's token
        current_token = players[current_player_index]
        
        # Display the board
        print_board(board)
        print(f"Player {current_token}'s turn")
        
        # Get player's column choice
        col = get_player_input()
        
        # Attempt to drop the piece
        if drop_piece(board, col, current_token):
            # Check if current player won
            if check_win(board, current_token):
                print_board(board)
                print(f"🎉 Player {current_token} wins! 🎉")
                break
            
            # Check if the game is a draw
            if check_draw(board):
                print_board(board)
                print("It's a draw! The board is full.")
                break
            
            # Move to next player
            current_player_index = (current_player_index + 1) % num_players
        else:
            # Column was full
            print("That column is full! Try another column.")
            input("Press Enter to continue...")

def main():
    """Main function to run the game with replay option."""
    while True:
        play_game()
        
        # Ask if players want to play again
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

# Run the game
if __name__ == "__main__":
    main()
