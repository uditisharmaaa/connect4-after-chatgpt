import os
import random

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
    """Display the game board."""
    os.system('clear')
    print("\n  Connect 4")
    print("  " + " ".join(COLUMN_LABELS))
    for i, row in enumerate(board):
        print(f"{i+1} " + " ".join(row))
    print()


def is_valid_column(column_input):
    """Check if the column input is valid."""
    return column_input.upper() in COLUMN_LABELS


def get_column_index(column_input):
    """Convert column letter to index."""
    return COLUMN_LABELS.index(column_input.upper())


def is_column_full(board, col):
    """Check if a column is full."""
    return board[0][col] != EMPTY


def drop_piece(board, col, symbol):
    """Drop a piece in the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    
    def check_direction(dr, dc):
        """Check for 4 in a row in a specific direction."""
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
    
    # Check horizontal, vertical, and both diagonals
    return (check_direction(0, 1) or   # Horizontal
            check_direction(1, 0) or   # Vertical
            check_direction(1, 1) or   # Diagonal /
            check_direction(1, -1))    # Diagonal \


def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != EMPTY for col in range(COLS))


def get_player_move(player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").strip()
        
        if not move:
            print("Please enter a column.")
            continue
        
        if not is_valid_column(move):
            print(f"Invalid column. Please choose A-G.")
            continue
        
        col = get_column_index(move)
        if is_column_full(board, col):
            print("That column is full. Choose another.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    # Validate number of players
    if not MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS:
        print(f"Error: NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
        return
    
    # Set up game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"Starting player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        
        # Get player move
        col = get_player_move(current_symbol)
        
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


if __name__ == "__main__":
    play_game()
