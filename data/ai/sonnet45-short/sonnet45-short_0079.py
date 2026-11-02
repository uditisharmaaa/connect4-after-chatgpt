# Connect 4 Game
# Intro CS Class Project

import random
import os

# CONSTANTS
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
    """Display the game board with column labels."""
    os.system('clear')
    print("\n=== CONNECT 4 ===\n")
    
    # Print column labels
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print("\n  " + "---" * COLS)
    
    # Print board rows (top to bottom)
    for row in range(ROWS):
        print(f"{row + 1} |", end="")
        for col in range(COLS):
            print(f" {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  " + "---" * COLS)
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

def get_column_input(player_symbol):
    """Get and validate column selection from player."""
    while True:
        choice = input(f"Player {player_symbol}, enter column (A-G): ").upper().strip()
        
        if len(choice) != 1:
            print("Please enter a single column letter.")
            continue
        
        if choice not in COLUMN_LABELS:
            print(f"Invalid column. Please choose from {', '.join(COLUMN_LABELS)}.")
            continue
        
        return COLUMN_LABELS.index(choice)

def drop_piece(board, col, symbol):
    """
    Drop a piece in the specified column.
    Returns the row where piece landed, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """
    Check if the last move at (row, col) created a win.
    Checks horizontal, vertical, and both diagonals.
    """
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == 4:
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
            if count == 4:
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
            if count == 4:
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

def play_game():
    """Main game loop."""
    # Setup
    board = create_board()
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    
    # Randomly select first player
    current_player_idx = random.randint(0, num_players - 1)
    
    print(f"\nPlayers: {', '.join(players)}")
    print(f"Starting player: {players[current_player_idx]}")
    input("\nPress Enter to start the game...")
    
    # Game loop
    moves_made = 0
    max_moves = ROWS * COLS
    
    while moves_made < max_moves:
        current_symbol = players[current_player_idx]
        print_board(board)
        
        # Get valid column input
        while True:
            col = get_column_input(current_symbol)
            row = drop_piece(board, col, current_symbol)
            
            if row == -1:
                print("That column is full! Choose another column.")
                continue
            break
        
        moves_made += 1
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} WINS! 🎉\n")
            return
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a DRAW! The board is full.\n")
            return
        
        # Move to next player
        current_player_idx = (current_player_idx + 1) % num_players

def main():
    """Main program entry point."""
    print("Welcome to Connect 4!")
    
    while True:
        play_game()
        
        play_again = input("Play again? (y/n): ").lower().strip()
        if play_again != 'y' and play_again != 'yes':
            print("\nThanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()
