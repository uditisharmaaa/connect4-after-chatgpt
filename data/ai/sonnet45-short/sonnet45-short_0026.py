import random
import os

# Constants for game configuration
NUM_ROWS = 6
NUM_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """
    Create and return an empty game board.
    The board is represented as a list of lists (2D array).
    Empty spaces are represented by '.'
    """
    board = []
    for row in range(NUM_ROWS):
        board.append(['.'] * NUM_COLS)
    return board

def display_board(board):
    """
    Display the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column labels
    print('\n  ', end='')
    for label in COLUMN_LABELS:
        print(label, end=' ')
    print('\n')
    
    # Print each row with its contents
    for row in board:
        print('  ', end='')
        for cell in row:
            print(cell, end=' ')
        print()
    print()

def get_column_input():
    """
    Get and validate column input from the player.
    Returns the column index (0-6) if valid, or None if invalid.
    """
    user_input = input("Enter column (A-G): ").strip().upper()
    
    # Check if input is a single character and is a valid column label
    if len(user_input) == 1 and user_input in COLUMN_LABELS:
        # Convert letter to column index (A->0, B->1, etc.)
        return COLUMN_LABELS.index(user_input)
    else:
        print("Invalid input! Please enter a column letter from A to G.")
        input("Press Enter to continue...")
        return None

def drop_piece(board, col, symbol):
    """
    Drop a piece into the specified column.
    Returns True if successful, False if column is full.
    The piece falls to the lowest available row in that column.
    """
    # Start from the bottom row and work upward
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == '.':
            board[row][col] = symbol
            return True
    
    # Column is full
    print("Column is full! Choose another column.")
    input("Press Enter to continue...")
    return False

def check_win(board, symbol):
    """
    Check if the specified symbol has won the game.
    Checks for 4 in a row horizontally, vertically, or diagonally.
    Returns True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == symbol and
                board[row][col + 1] == symbol and
                board[row][col + 2] == symbol and
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == symbol and
                board[row + 1][col] == symbol and
                board[row + 2][col] == symbol and
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == symbol and
                board[row - 1][col + 1] == symbol and
                board[row - 2][col + 2] == symbol and
                board[row - 3][col + 3] == symbol):
                return True
    
    return False

def check_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    Returns True if the board is full, False otherwise.
    """
    # Check if the top row has any empty spaces
    for col in range(NUM_COLS):
        if board[0][col] == '.':
            return False
    return True

def get_number_of_players():
    """
    Get the number of players from the user.
    Validates that the number is between MIN_PLAYERS and MAX_PLAYERS.
    """
    while True:
        try:
            num_players = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                return num_players
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def play_game():
    """
    Main game loop that controls the flow of the game.
    """
    # Setup: get number of players and create the board
    num_players = get_number_of_players()
    players = PLAYER_SYMBOLS[:num_players]
    board = create_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    print(f"\nPlayer {players[current_player_index]} will go first!")
    input("Press Enter to start the game...")
    
    # Main game loop
    while True:
        # Get current player's symbol
        current_symbol = players[current_player_index]
        
        # Display the board
        display_board(board)
        
        # Show whose turn it is
        print(f"Player {current_symbol}'s turn")
        
        # Get valid move from player
        col = None
        while col is None:
            col = get_column_input()
            
            # If valid column, try to drop the piece
            if col is not None:
                if not drop_piece(board, col, current_symbol):
                    col = None  # Reset if column was full
        
        # Check for win
        if check_win(board, current_symbol):
            display_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        # Check for draw
        if check_draw(board):
            display_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player (cycle through players)
        current_player_index = (current_player_index + 1) % num_players

def main():
    """
    Main function to start the game and handle replay.
    """
    print("=" * 30)
    print("   Welcome to Connect 4!")
    print("=" * 30)
    print("\nGet 4 in a row to win!")
    print("(Horizontal, Vertical, or Diagonal)\n")
    
    # Game loop - allows playing multiple games
    while True:
        play_game()
        
        # Ask if players want to play again
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            break

# Run the game when the script is executed
if __name__ == "__main__":
    main()
