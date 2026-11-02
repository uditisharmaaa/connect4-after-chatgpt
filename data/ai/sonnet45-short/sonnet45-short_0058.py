import random
import os

# Game constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty game board (6 rows x 7 columns)"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the current game board with column labels"""
    os.system('clear')  # Clear the screen for a clean display
    
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print(' ' + '---' * COLS + '--')
    
    # Print each row with row numbers
    for i in range(ROWS):
        row_display = str(i + 1) + '| '
        for j in range(COLS):
            row_display += board[i][j] + ' | '
        print(row_display)
        print(' ' + '---' * COLS + '--')

def drop_piece(board, col, symbol):
    """
    Drop a piece in the specified column.
    Returns True if successful, False if column is full.
    """
    # Start from bottom row and work up to find empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False  # Column is full

def check_win(board, symbol):
    """
    Check if the given player symbol has won.
    Checks horizontal, vertical, and both diagonal directions.
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row][col + 1] == symbol and
                board[row][col + 2] == symbol and
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and
                board[row + 1][col] == symbol and
                board[row + 2][col] == symbol and
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row - 1][col + 1] == symbol and
                board[row - 2][col + 2] == symbol and
                board[row - 3][col + 3] == symbol):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)"""
    # If top row has any empty spaces, game is not a draw
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_valid_input(current_player):
    """
    Get and validate player input for column selection.
    Returns the column index (0-6) for a valid move.
    """
    while True:
        choice = input(f"Player {current_player}, enter column (A-G): ").upper().strip()
        
        # Check if input is a valid column label
        if choice not in COLUMN_LABELS:
            print(f"Invalid input! Please enter a column letter from A to G.")
            continue
        
        # Convert letter to column index
        col_index = COLUMN_LABELS.index(choice)
        return col_index

def play_game():
    """Main game loop"""
    # Initialize the game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]  # Get only the symbols needed
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\n=== Connect 4 Game ===")
    print(f"Players: {', '.join(players)}")
    print(f"Starting player: {players[current_player_index]}")
    input("\nPress Enter to start...")
    
    # Game loop continues until someone wins or board is full
    while True:
        current_player = players[current_player_index]
        
        # Display the current board
        print_board(board)
        
        # Get player's move
        col_index = get_valid_input(current_player)
        
        # Attempt to drop the piece
        if not drop_piece(board, col_index, current_player):
            print("That column is full! Try another column.")
            input("Press Enter to continue...")
            continue
        
        # Check if current player won
        if check_win(board, current_player):
            print_board(board)
            print(f"\n🎉 Player {current_player} wins! 🎉")
            break
        
        # Check if the game is a draw
        if check_draw(board):
            print_board(board)
            print("\n🤝 It's a draw! The board is full. 🤝")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Entry point of the program"""
    while True:
        play_game()
        
        # Ask if players want to play again
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("Thanks for playing!")
            break

# Run the game
if __name__ == "__main__":
    main()
