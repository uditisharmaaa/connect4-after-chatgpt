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
    """Create and return an empty game board."""
    # Create a 2D list filled with spaces representing empty cells
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Display the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print(' +' + '---+' * NUM_COLS)
    
    # Print each row with row numbers
    for i, row in enumerate(board):
        print(str(i) + '| ' + ' | '.join(row) + ' |')
        print(' +' + '---+' * NUM_COLS)
    print()

def get_column_input():
    """Get and validate column input from the player."""
    while True:
        choice = input(f"Choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[NUM_COLS-1]}): ").strip().upper()
        
        # Check if input is a valid column label
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)  # Return column index (0-6)
        else:
            print(f"Invalid input. Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[NUM_COLS-1]}.")

def drop_piece(board, col, symbol):
    """
    Drop a piece into the specified column.
    Returns the row where the piece landed, or -1 if column is full.
    """
    # Start from the bottom row and work upward
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1  # Column is full

def check_win(board, row, col, symbol):
    """
    Check if the last move at (row, col) created a winning condition.
    Checks horizontal, vertical, and both diagonal directions.
    """
    
    # Helper function to count consecutive pieces in a given direction
    def count_direction(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        
        # Keep counting while within bounds and matching symbol
        while (0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and 
               board[r][c] == symbol):
            count += 1
            r += delta_row
            c += delta_col
        return count
    
    # Check horizontal (left + right + 1 for current piece)
    horizontal = count_direction(0, -1) + count_direction(0, 1) + 1
    
    # Check vertical (down + up + 1 for current piece)
    vertical = count_direction(1, 0) + count_direction(-1, 0) + 1
    
    # Check diagonal (bottom-left to top-right)
    diagonal1 = count_direction(1, -1) + count_direction(-1, 1) + 1
    
    # Check diagonal (top-left to bottom-right)
    diagonal2 = count_direction(-1, -1) + count_direction(1, 1) + 1
    
    # Win condition: 4 or more in a row in any direction
    return horizontal >= 4 or vertical >= 4 or diagonal1 >= 4 or diagonal2 >= 4

def check_draw(board):
    """Check if the board is full (draw condition)."""
    # Check if top row has any empty spaces
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    # Get number of players
    while True:
        try:
            num_players = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                break
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Set up players with their symbols
    players = PLAYER_SYMBOLS[:num_players]
    print(f"\nPlayers: {', '.join(players)}")
    input("Press Enter to start the game...")
    
    # Initialize game board
    board = create_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    print(f"\n{players[current_player_index]} goes first!")
    
    # Main game loop
    while True:
        current_symbol = players[current_player_index]
        
        # Display the board
        print_board(board)
        print(f"Player {current_symbol}'s turn")
        
        # Get valid column input
        col = get_column_input()
        
        # Attempt to drop the piece
        row = drop_piece(board, col, current_symbol)
        
        # Check if column was full
        if row == -1:
            print("That column is full! Choose another column.")
            input("Press Enter to continue...")
            continue
        
        # Check for win condition
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        # Check for draw condition
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players

def main():
    """Entry point for the game."""
    print("=" * 40)
    print("       WELCOME TO CONNECT 4!")
    print("=" * 40)
    print("\nConnect 4 pieces in a row to win!")
    print("(Horizontally, vertically, or diagonally)\n")
    
    # Play the game
    play_game()
    
    # Ask if players want to play again
    while True:
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again == 'y':
            play_game()
        elif again == 'n':
            print("Thanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'.")

# Run the game
if __name__ == "__main__":
    main()
