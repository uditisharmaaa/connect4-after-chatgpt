import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2-5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the current game board."""
    print('\n  ' + ' '.join(COLUMN_LABELS))
    print(' +' + '-' * (COLS * 2 - 1) + '+')
    
    for row in board:
        print(' |' + '|'.join(row) + '|')
    
    print(' +' + '-' * (COLS * 2 - 1) + '+')
    print('  ' + ' '.join(COLUMN_LABELS))
    print()

def get_column_input(current_player):
    """Get and validate column input from the player."""
    while True:
        user_input = input(f"Player {current_player}, choose a column (A-G): ").upper().strip()
        
        if user_input in COLUMN_LABELS:
            return COLUMN_LABELS.index(user_input)
        else:
            print(f"Invalid input! Please enter a letter between A and G.")

def drop_piece(board, col, symbol):
    """
    Drop a piece in the specified column.
    Returns the row where the piece landed, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) created a win."""
    
    # Check horizontal
    def check_direction(delta_row, delta_col):
        count = 1  # Count the piece we just placed
        
        # Check in positive direction
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += delta_row
            c += delta_col
        
        # Check in negative direction
        r, c = row - delta_row, col - delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= delta_row
            c -= delta_col
        
        return count >= 4
    
    # Check all four directions: horizontal, vertical, diagonal /, diagonal \
    if check_direction(0, 1):  # Horizontal
        return True
    if check_direction(1, 0):  # Vertical
        return True
    if check_direction(1, 1):  # Diagonal \
        return True
    if check_direction(1, -1):  # Diagonal /
        return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    os.system('clear')
    print("=" * 40)
    print("        WELCOME TO CONNECT 4!")
    print("=" * 40)
    print(f"\nNumber of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(players)}")
    print(f"\nPlayer {players[current_player_index]} goes first!")
    input("\nPress Enter to start...")
    
    # Game loop
    while True:
        os.system('clear')
        current_symbol = players[current_player_index]
        
        print_board(board)
        
        # Get valid column input
        while True:
            col = get_column_input(current_symbol)
            row = drop_piece(board, col, current_symbol)
            
            if row != -1:
                break
            else:
                print("That column is full! Choose another column.")
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            os.system('clear')
            print_board(board)
            print("=" * 40)
            print(f"   Player {current_symbol} WINS!")
            print("=" * 40)
            break
        
        # Check for draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("=" * 40)
            print("        IT'S A DRAW!")
            print("=" * 40)
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main function to run the game with replay option."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("\nThanks for playing Connect 4!")
            break

if __name__ == "__main__":
    main()
