# Connect 4 Game
# Intro CS Class Project

import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
WIN_CONDITION = 4  # Number in a row to win

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print("\n=== CONNECT 4 ===\n")
    
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    # Print rows from top to bottom
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(col_input):
    """Check if the column input is valid."""
    col_input = col_input.strip().upper()
    return col_input in COLUMN_LABELS

def get_column_index(col_input):
    """Convert column letter to index."""
    return COLUMN_LABELS.index(col_input.strip().upper())

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != ' '

def drop_piece(board, col_index, symbol):
    """Drop a piece in the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, enter column (A-G): ")
        
        # Validate input format
        if not move:
            print("Invalid input! Please enter a column letter (A-G).")
            continue
        
        if not is_valid_column(move):
            print("Invalid column! Please enter a letter from A to G.")
            continue
        
        col_index = get_column_index(move)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("That column is full! Please choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Pick random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("\nPress Enter to start...")
    
    # Game loop
    moves_made = 0
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        
        # Get player move
        col_index = get_player_move(board, current_symbol)
        
        # Drop piece
        row = drop_piece(board, col_index, current_symbol)
        moves_made += 1
        
        # Check for win (only possible after 7 moves minimum)
        if moves_made >= 7:
            if check_win(board, row, col_index, current_symbol):
                print_board(board)
                print(f"🎉 Player {current_symbol} WINS! 🎉")
                break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a DRAW! The board is full.")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main function to run the game."""
    while True:
        play_game()
        
        # Ask to play again
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing Connect 4!")
            break

if __name__ == "__main__":
    main()
