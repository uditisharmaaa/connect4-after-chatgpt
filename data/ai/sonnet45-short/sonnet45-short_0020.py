import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(board, col):
    """Check if a column has space for a piece."""
    return 0 <= col < COLS and board[0][col] == ' '

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    # Check horizontal
    def check_direction(dr, dc):
        count = 0
        # Check in positive direction
        r, c = row, col
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
    return (check_direction(0, 1) or   # Horizontal
            check_direction(1, 0) or   # Vertical
            check_direction(1, 1) or   # Diagonal \
            check_direction(1, -1))    # Diagonal /

def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        try:
            move = input(f"Player {player_symbol}, enter column (A-G): ").strip().upper()
            
            if len(move) != 1 or move not in COLUMN_LABELS:
                print("Invalid input! Please enter a letter A-G.")
                input("Press Enter to continue...")
                continue
            
            col = COLUMN_LABELS.index(move)
            
            if not is_valid_column(board, col):
                print("Column is full! Choose another column.")
                input("Press Enter to continue...")
                continue
            
            return col
        except (ValueError, IndexError):
            print("Invalid input! Please enter a letter A-G.")
            input("Press Enter to continue...")

def play_game():
    """Main game loop."""
    # Setup
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        
        # Get player move
        col = get_player_move(board, current_symbol)
        
        # Drop piece
        row = drop_piece(board, col, current_symbol)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Entry point of the program."""
    while True:
        play_game()
        replay = input("\nPlay again? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
