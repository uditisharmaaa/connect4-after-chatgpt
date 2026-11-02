import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 for different number of players
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print("\n  " + "   ".join(COLUMN_LABELS))
    print("  " + "---" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("  " + "---" * COLS)
    print()


def is_valid_move(board, col):
    """Check if a move is valid (column has space)."""
    return board[0][col] == ' '


def get_next_row(board, col):
    """Find the lowest empty row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1


def drop_piece(board, row, col, player):
    """Place a player's piece on the board."""
    board[row][col] = player


def check_win(board, player):
    """Check if the current player has won."""
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


def is_board_full(board):
    """Check if the board is completely filled (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))


def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player}, enter column (A-G): ").strip().upper()
        
        # Validate input is a single character
        if len(move) != 1:
            print("Invalid input! Please enter a single column letter (A-G).")
            continue
        
        # Validate input is a valid column label
        if move not in COLUMN_LABELS:
            print("Invalid column! Please choose A-G.")
            continue
        
        # Convert letter to column index
        col = COLUMN_LABELS.index(move)
        
        # Validate column is not full
        if not is_valid_move(board, col):
            print("Column is full! Choose another column.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    board = create_board()
    
    # Pick random first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"First player: {PLAYERS[current_player_idx]}")
    input("Press Enter to start...")
    
    game_over = False
    
    while not game_over:
        current_player = PLAYERS[current_player_idx]
        print_board(board)
        
        # Get player move
        col = get_player_move(board, current_player)
        
        # Drop piece
        row = get_next_row(board, col)
        drop_piece(board, row, col, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()
    
    # Ask to play again
    while True:
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again == 'y':
            play_game()
        elif again == 'n':
            print("Thanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()
