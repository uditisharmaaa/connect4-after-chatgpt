import random
import os

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Game configuration
NUM_PLAYERS = 2  # Change this to 2-5 players


def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the current state of the board."""
    os.system('clear')
    print("\n  CONNECT 4\n")
    
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    # Print each row
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()


def drop_piece(board, col, symbol):
    """
    Drop a piece in the specified column.
    Returns True if successful, False if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False


def is_valid_column(board, col):
    """Check if a column is valid and not full."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '


def get_column_input():
    """
    Get and validate column input from the player.
    Returns the column index (0-6) or -1 if invalid.
    """
    user_input = input("Enter column (A-G): ").strip().upper()
    
    if len(user_input) != 1 or user_input not in COLUMN_LABELS:
        return -1
    
    return COLUMN_LABELS.index(user_input)


def check_win(board, symbol):
    """Check if the specified symbol has won the game."""
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))


def play_game():
    """Main game loop."""
    # Validate number of players
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Error: NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
        return
    
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"Starting game with {NUM_PLAYERS} players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        print(f"Player {current_symbol}'s turn")
        
        # Get valid column input
        while True:
            col = get_column_input()
            
            if col == -1:
                print("Invalid input! Please enter a letter from A to G.")
                continue
            
            if not is_valid_column(board, col):
                print("Column is full! Choose another column.")
                continue
            
            break
        
        # Drop the piece
        drop_piece(board, col, current_symbol)
        
        # Check for win
        if check_win(board, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
