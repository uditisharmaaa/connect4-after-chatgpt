import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this between 2-5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    print('\n  ' + ' '.join(COLUMN_LABELS))
    print(' +' + '-' * (COLS * 2 - 1) + '+')
    for row in board:
        print(' |' + '|'.join(row) + '|')
    print(' +' + '-' * (COLS * 2 - 1) + '+')
    print()

def get_column_input(player_symbol):
    """Get and validate column input from player."""
    while True:
        user_input = input(f"Player {player_symbol}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}): ").upper().strip()
        
        if user_input not in COLUMN_LABELS[:COLS]:
            print(f"Invalid input! Please choose from {COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}.")
            continue
        
        return COLUMN_LABELS.index(user_input)

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column. Returns True if successful, False if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False

def check_win(board, symbol):
    """Check if the given symbol has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row][col+1] == symbol and 
                board[row][col+2] == symbol and 
                board[row][col+3] == symbol):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and 
                board[row+1][col] == symbol and 
                board[row+2][col] == symbol and 
                board[row+3][col] == symbol):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row-1][col+1] == symbol and 
                board[row-2][col+2] == symbol and 
                board[row-3][col+3] == symbol):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row+1][col+1] == symbol and 
                board[row+2][col+2] == symbol and 
                board[row+3][col+3] == symbol):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    # Validate number of players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5!")
        return
    
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    os.system('clear')
    print("=" * 30)
    print("    WELCOME TO CONNECT 4!")
    print("=" * 30)
    print(f"\nPlayers: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    print("\nConnect 4 pieces in a row to win!")
    input("\nPress Enter to start...")
    
    # Game loop
    while True:
        os.system('clear')
        print_board(board)
        
        current_symbol = players[current_player_index]
        
        # Get valid column input
        while True:
            col = get_column_input(current_symbol)
            if drop_piece(board, col, current_symbol):
                break
            else:
                print("That column is full! Choose another column.")
        
        # Check for win
        if check_win(board, current_symbol):
            os.system('clear')
            print_board(board)
            print("=" * 30)
            print(f"  Player {current_symbol} WINS!")
            print("=" * 30)
            break
        
        # Check for draw
        if is_board_full(board):
            os.system('clear')
            print_board(board)
            print("=" * 30)
            print("    IT'S A DRAW!")
            print("=" * 30)
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main function to run the game."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("\nThanks for playing!")
            break

if __name__ == "__main__":
    main()
