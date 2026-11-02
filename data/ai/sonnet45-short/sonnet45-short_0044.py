# Connect 4 Game
# For Intro CS Class

import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H'] for 4 players, etc.
EMPTY = '.'

def create_board():
    """Create and return an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  " + " ".join(COLUMN_LABELS))
    for i, row in enumerate(board):
        print(f"{i+1} " + " ".join(row))
    print()

def is_valid_column(column, board):
    """Check if a column choice is valid."""
    # Check if column letter is valid
    if column.upper() not in COLUMN_LABELS:
        return False
    
    col_index = COLUMN_LABELS.index(column.upper())
    
    # Check if column has space
    return board[0][col_index] == EMPTY

def drop_piece(board, column, player):
    """Drop a piece in the specified column. Return the row where it landed."""
    col_index = COLUMN_LABELS.index(column.upper())
    
    # Find the lowest empty row in this column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            board[row][col_index] = player
            return row
    
    return -1  # Column is full (shouldn't happen if validated)

def check_win(board, player):
    """Check if the specified player has won."""
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row][col+1] == player and
                board[row][col+2] == player and
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and
                board[row+1][col] == player and
                board[row+2][col] == player and
                board[row+3][col] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row-1][col+1] == player and
                board[row-2][col+2] == player and
                board[row-3][col+3] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row+1][col+1] == player and
                board[row+2][col+2] == player and
                board[row+3][col+3] == player):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == EMPTY:
            return False
    return True

def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        column = input(f"Player {player}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").strip()
        
        if is_valid_column(column, board):
            return column.upper()
        else:
            print("Invalid move! Column is either full or doesn't exist. Try again.")
            input("Press Enter to continue...")

def play_game():
    """Main game loop."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"First player: {PLAYERS[current_player_index]}")
    input("Press Enter to start...")
    
    game_over = False
    
    while not game_over:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        # Get player move
        column = get_player_move(board, current_player)
        
        # Drop the piece
        drop_piece(board, column, current_player)
        
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
            current_player_index = (current_player_index + 1) % len(PLAYERS)
    
    print("\nThanks for playing!")

def main():
    """Entry point of the program."""
    play_game()
    
    # Ask if they want to play again
    while True:
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again == 'y':
            play_game()
        elif play_again == 'n':
            print("Goodbye!")
            break
        else:
            print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
