import random
import os

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the current game board."""
    print("\n  " + "   ".join(COLUMN_LABELS))
    print("  " + "---" * COLS + "--")
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("  " + "---" * COLS + "--")
    print()

def get_num_players():
    """Get and validate the number of players."""
    while True:
        try:
            num = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num <= MAX_PLAYERS:
                return num
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_column_input():
    """Get and validate column choice from user."""
    while True:
        choice = input("Enter column (A-G): ").upper().strip()
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        else:
            print("Invalid column. Please choose A-G.")

def is_valid_move(board, col):
    """Check if a move is valid (column not full)."""
    return board[0][col] == ' '

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_winner(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    def check_direction(dr, dc):
        count = 1  # Count the piece we just placed
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        
        return count >= 4
    
    # Check all four directions: horizontal, vertical, diagonal /, diagonal \
    return (check_direction(0, 1) or  # Horizontal
            check_direction(1, 0) or  # Vertical
            check_direction(1, 1) or  # Diagonal \
            check_direction(1, -1))   # Diagonal /

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    os.system('clear')
    print("=" * 30)
    print("   WELCOME TO CONNECT 4!")
    print("=" * 30)
    print("\nConnect 4 pieces in a row to win!")
    print("(Horizontal, Vertical, or Diagonal)\n")
    
    # Setup
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    board = create_board()
    
    # Randomly select first player
    current_player_idx = random.randint(0, num_players - 1)
    
    print(f"\nPlayers: {', '.join(players)}")
    print(f"Player {players[current_player_idx]} goes first!")
    input("\nPress Enter to start...")
    
    # Game loop
    move_count = 0
    while True:
        os.system('clear')
        print_board(board)
        
        current_symbol = players[current_player_idx]
        print(f"Player {current_symbol}'s turn")
        
        # Get valid move
        while True:
            col = get_column_input()
            if is_valid_move(board, col):
                break
            else:
                print("That column is full! Choose another.")
        
        # Make move
        row = drop_piece(board, col, current_symbol)
        move_count += 1
        
        # Check for winner
        if check_winner(board, row, col, current_symbol):
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
            print("     IT'S A DRAW!")
            print("=" * 30)
            break
        
        # Next player
        current_player_idx = (current_player_idx + 1) % num_players

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
