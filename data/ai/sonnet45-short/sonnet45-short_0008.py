import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  Connect 4 Game")
    print("=" * 29)
    
    # Column labels
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(label, end="   ")
    print("\n" + "  " + "----" * COLS)
    
    # Board rows (top to bottom)
    for row in board:
        print("| ", end="")
        for cell in row:
            print(cell + " | ", end="")
        print("\n" + "  " + "----" * COLS)
    print()

def drop_piece(board, col, player):
    """Drop a piece in the specified column. Returns True if successful."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def is_valid_column(board, col):
    """Check if a column has space for a piece."""
    return board[0][col] == ' '

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row][col + 1] == player and
                board[row][col + 2] == player and
                board[row][col + 3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and
                board[row + 1][col] == player and
                board[row + 2][col] == player and
                board[row + 3][col] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row - 1][col + 1] == player and
                board[row - 2][col + 2] == player and
                board[row - 3][col + 3] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player}, enter column (A-G): ").strip().upper()
        
        # Validate input
        if len(move) != 1 or move not in COLUMN_LABELS:
            print("Invalid input! Please enter a letter from A to G.")
            continue
        
        col_index = COLUMN_LABELS.index(move)
        
        # Check if column is full
        if not is_valid_column(board, col_index):
            print("Column is full! Choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    board = create_board()
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\nWelcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"Starting player: {PLAYERS[current_player_index]}")
    input("\nPress Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        # Get player move
        col = get_player_move(board, current_player)
        
        # Drop piece
        drop_piece(board, col, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Run the game with option to play again."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
