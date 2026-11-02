import random
import os

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Game configuration
NUM_PLAYERS = 3  # Change this between 2 and 5


def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  Connect 4\n")
    
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    # Print rows (from top to bottom)
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()


def drop_piece(board, col, token):
    """
    Drop a piece into the specified column.
    Returns the row where the piece landed, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return row
    return -1


def is_valid_column(col_input):
    """Check if the input is a valid column label."""
    return col_input.upper() in COLUMN_LABELS


def is_column_available(board, col):
    """Check if the column has space for another piece."""
    return board[0][col] == ' '


def check_winner(board, row, col, token):
    """
    Check if the last move at (row, col) created a winning connection.
    Checks horizontal, vertical, and both diagonals.
    """
    # Horizontal check
    count = 0
    for c in range(COLS):
        if board[row][c] == token:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Vertical check
    count = 0
    for r in range(ROWS):
        if board[r][col] == token:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Diagonal check (down-right)
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    count = 0
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == token:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Diagonal check (up-right)
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    count = 0
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == token:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))


def get_player_move(board, player_token):
    """
    Get and validate player input.
    Returns the column index (0-6).
    """
    while True:
        col_input = input(f"Player {player_token}, choose column (A-G): ").strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input! Please enter a letter from A to G.")
            continue
        
        col_index = COLUMN_LABELS.index(col_input)
        
        if not is_column_available(board, col_index):
            print("That column is full! Choose another column.")
            continue
        
        return col_index


def play_game():
    """Main game loop."""
    # Validate number of players
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Error: NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
        return
    
    # Setup
    board = create_board()
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Players: {', '.join(players)}")
    print(f"Starting player: {players[current_player_index]}\n")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_token = players[current_player_index]
        print_board(board)
        
        # Get player move
        col = get_player_move(board, current_token)
        
        # Drop piece
        row = drop_piece(board, col, current_token)
        
        # Check for winner
        if check_winner(board, row, col, current_token):
            print_board(board)
            print(f"🎉 Player {current_token} wins! 🎉\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Entry point of the game."""
    play_game()
    
    # Ask to play again
    play_again = input("Play again? (y/n): ").strip().lower()
    if play_again == 'y':
        main()


if __name__ == "__main__":
    main()
