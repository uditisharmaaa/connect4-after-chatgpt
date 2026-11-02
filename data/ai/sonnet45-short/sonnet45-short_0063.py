# Connect 4 Game
# A multi-player Connect 4 game supporting 2-5 players

import os
import random

# CONSTANTS
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
EMPTY = '.'

def create_board():
    """Create and return an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the current game board."""
    os.system('clear')
    print("\n=== CONNECT 4 ===\n")
    
    # Print column labels
    print("  " + " ".join(COLUMN_LABELS))
    
    # Print each row with row numbers
    for i, row in enumerate(board):
        print(f"{i+1} " + " ".join(row))
    
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
    """Get and validate column input from player."""
    while True:
        col_input = input(f"Player {player_symbol}, enter column (A-G): ").strip().upper()
        
        if len(col_input) != 1:
            print("Please enter a single column letter.")
            continue
        
        if col_input not in COLUMN_LABELS:
            print(f"Invalid column. Please enter a letter from A to G.")
            continue
        
        return COLUMN_LABELS.index(col_input)

def drop_piece(board, col, symbol):
    """
    Drop a piece in the specified column.
    Returns the row where piece was placed, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """
    Check if the last move at (row, col) created a win for symbol.
    Checks horizontal, vertical, and both diagonals.
    """
    # Directions: horizontal, vertical, diagonal-down, diagonal-up
    directions = [
        [(0, 1), (0, -1)],   # Horizontal
        [(1, 0), (-1, 0)],   # Vertical
        [(1, 1), (-1, -1)],  # Diagonal \
        [(1, -1), (-1, 1)]   # Diagonal /
    ]
    
    for direction_pair in directions:
        count = 1  # Count the piece we just placed
        
        # Check both directions
        for dr, dc in direction_pair:
            r, c = row + dr, col + dc
            
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
                count += 1
                r += dr
                c += dc
        
        if count >= 4:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != EMPTY for col in range(COLS))

def play_game():
    """Main game loop."""
    # Setup
    board = create_board()
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    
    # Randomly select first player
    current_player_idx = random.randint(0, num_players - 1)
    
    print(f"\nPlayers: {', '.join(players)}")
    print(f"First player: {players[current_player_idx]}")
    input("\nPress Enter to start...")
    
    # Game loop
    moves_made = 0
    max_moves = ROWS * COLS
    
    while moves_made < max_moves:
        print_board(board)
        current_symbol = players[current_player_idx]
        
        # Get valid move
        while True:
            col = get_column_input(current_symbol)
            row = drop_piece(board, col, current_symbol)
            
            if row != -1:
                break
            else:
                print("That column is full! Choose another column.")
        
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
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

def main():
    """Main program entry point."""
    while True:
        play_game()
        
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
