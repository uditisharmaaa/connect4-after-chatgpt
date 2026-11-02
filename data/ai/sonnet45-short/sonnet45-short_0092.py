import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O']  # Change this to add more players: ['X', 'O', 'V', 'H', 'M']
EMPTY = '.'

def create_board():
    """Create an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  Connect 4\n")
    
    # Print column labels
    print("  " + " ".join(COLUMN_LABELS))
    
    # Print rows
    for i, row in enumerate(board):
        print(f"{i+1} " + " ".join(row))
    
    print()

def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper().strip()
        
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        else:
            print("Invalid input! Please enter a letter from A to G.")

def drop_piece(board, col, player):
    """Drop a piece in the specified column. Returns True if successful."""
    # Start from bottom row and go up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True
    
    # Column is full
    return False

def check_win(board, player):
    """Check if the player has won."""
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row][col+1] == player and
                board[row][col+2] == player and
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and
                board[row+1][col] == player and
                board[row+2][col] == player and
                board[row+3][col] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row+1][col+1] == player and
                board[row+2][col+2] == player and
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row-1][col+1] == player and
                board[row-2][col+2] == player and
                board[row-3][col+3] == player):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for row in board:
        if EMPTY in row:
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    
    # Pick random first player
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    print(f"Player {PLAYERS[current_player_index]} goes first!\n")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        # Get player input
        col = get_column_input(current_player)
        
        # Try to drop piece
        if not drop_piece(board, col, current_player):
            print("That column is full! Try another column.")
            input("Press Enter to continue...")
            continue
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉\n")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

def main():
    """Main function to run the game."""
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}\n")
    
    play_game()
    
    # Ask to play again
    play_again = input("Play again? (y/n): ").lower().strip()
    if play_again == 'y':
        main()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    main()
