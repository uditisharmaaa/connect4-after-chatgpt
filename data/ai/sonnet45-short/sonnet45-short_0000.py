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
    print("\n  CONNECT 4")
    print("  " + " ".join(COLUMN_LABELS))
    print("  " + "-" * (COLS * 2 - 1))
    for row in board:
        print("| " + " ".join(row) + " |")
    print("  " + "-" * (COLS * 2 - 1))
    print("  " + " ".join(COLUMN_LABELS))
    print()

def is_valid_move(board, col):
    """Check if a move is valid (column not full)."""
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """Find the next open row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def drop_piece(board, row, col, piece):
    """Place a piece on the board."""
    board[row][col] = piece

def check_win(board, piece):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == piece and
                board[row][col + 1] == piece and
                board[row][col + 2] == piece and
                board[row][col + 3] == piece):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == piece and
                board[row + 1][col] == piece and
                board[row + 2][col] == piece and
                board[row + 3][col] == piece):
                return True
    
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == piece and
                board[row + 1][col + 1] == piece and
                board[row + 2][col + 2] == piece and
                board[row + 3][col + 3] == piece):
                return True
    
    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == piece and
                board[row - 1][col + 1] == piece and
                board[row - 2][col + 2] == piece and
                board[row - 3][col + 3] == piece):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_column_input():
    """Get and validate column input from player."""
    while True:
        col_input = input("Enter column (A-G): ").upper().strip()
        if col_input in COLUMN_LABELS:
            return COLUMN_LABELS.index(col_input)
        else:
            print("Invalid input! Please enter a letter from A to G.")

def play_game():
    """Main game loop."""
    board = create_board()
    game_over = False
    
    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Starting player: {PLAYERS[current_player_idx]}")
    input("Press Enter to continue...")
    
    while not game_over:
        print_board(board)
        current_piece = PLAYERS[current_player_idx]
        print(f"Player {current_piece}'s turn")
        
        # Get valid column input
        col = get_column_input()
        
        # Check if move is valid
        if is_valid_move(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, current_piece)
            
            # Check for win
            if check_win(board, current_piece):
                print_board(board)
                print(f"🎉 Player {current_piece} wins! 🎉")
                game_over = True
            # Check for draw
            elif is_board_full(board):
                print_board(board)
                print("It's a draw! The board is full.")
                game_over = True
            else:
                # Move to next player
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            print(f"Column {COLUMN_LABELS[col]} is full! Try another column.")
            input("Press Enter to continue...")

def main():
    """Main function to run the game."""
    print("Welcome to Connect 4!")
    print(f"Number of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(PLAYERS)}")
    input("\nPress Enter to start the game...")
    
    play_again = 'y'
    while play_again.lower() == 'y':
        play_game()
        play_again = input("\nDo you want to play again? (y/n): ")
    
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
