import random
import os

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
EMPTY = '.'

# Number of players (change this between 2-5)
NUM_PLAYERS = 2


def create_board():
    """Create and return an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print("\n  " + " ".join(COLUMN_LABELS))
    print("  " + "-" * (COLS * 2 - 1))
    for row in board:
        print("  " + " ".join(row))
    print()


def is_valid_column(board, col_index):
    """Check if a column has space for a new piece."""
    return 0 <= col_index < COLS and board[0][col_index] == EMPTY


def drop_piece(board, col_index, symbol):
    """Drop a piece into the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            board[row][col_index] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) created a winning condition."""
    
    def check_direction(delta_row, delta_col):
        """Count consecutive pieces in both directions."""
        count = 1  # Count the piece just placed
        
        # Check positive direction
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += delta_row
            c += delta_col
        
        # Check negative direction
        r, c = row - delta_row, col - delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= delta_row
            c -= delta_col
        
        return count >= 4
    
    # Check all four directions: horizontal, vertical, and two diagonals
    return (check_direction(0, 1) or   # Horizontal
            check_direction(1, 0) or   # Vertical
            check_direction(1, 1) or   # Diagonal /
            check_direction(1, -1))    # Diagonal \


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != EMPTY for col in range(COLS))


def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, enter column (A-G): ").strip().upper()
        
        if len(move) != 1 or move not in COLUMN_LABELS:
            print(f"Invalid input. Please enter a letter from A to G.")
            continue
        
        col_index = COLUMN_LABELS.index(move)
        
        if not is_valid_column(board, col_index):
            print(f"Column {move} is full. Choose another column.")
            continue
        
        return col_index


def play_game():
    """Main game loop."""
    # Validate number of players
    if not (MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS):
        print(f"Error: NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
        return
    
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\n=== Connect 4 ===")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        
        # Get player move
        col_index = get_player_move(board, current_symbol)
        
        # Drop piece
        row = drop_piece(board, col_index, current_symbol)
        
        # Check for win
        if check_win(board, row, col_index, current_symbol):
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
    """Entry point for the game."""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
