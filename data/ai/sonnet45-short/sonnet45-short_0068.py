import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  " + "   ".join(COLUMN_LABELS))
    print("  " + "---" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("  " + "---" * COLS)
    print()

def get_column_input():
    """Get and validate column input from player."""
    while True:
        user_input = input(f"Enter column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}): ").upper().strip()
        
        if user_input in COLUMN_LABELS:
            return COLUMN_LABELS.index(user_input)
        else:
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[COLS-1]}.")

def is_column_full(board, col):
    """Check if a column is full."""
    return board[0][col] != ' '

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    
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

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    # Set up players
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Create board
    board = create_board()
    
    print("=" * 40)
    print("         CONNECT 4 GAME")
    print("=" * 40)
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    print("\nConnect 4 pieces in a row to win!")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        
        # Display board
        print_board(board)
        print(f"Player {current_symbol}'s turn")
        
        # Get valid move
        while True:
            col = get_column_input()
            
            if is_column_full(board, col):
                print("That column is full! Choose another.")
            else:
                break
        
        # Drop piece
        row = drop_piece(board, col, current_symbol)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print("=" * 40)
            print(f"  🎉 Player {current_symbol} WINS! 🎉")
            print("=" * 40)
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("=" * 40)
            print("     DRAW! The board is full!")
            print("=" * 40)
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main function to run the game."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("\nThanks for playing Connect 4!")
            break

if __name__ == "__main__":
    main()
