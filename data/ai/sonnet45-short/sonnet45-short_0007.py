# Connect 4 Game
# A multi-player Connect 4 implementation with 2-5 players

import os
import random

# ============================================================================
# CONSTANTS
# ============================================================================
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

# ============================================================================
# BOARD FUNCTIONS
# ============================================================================

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def display_board(board):
    """Display the current state of the board."""
    os.system('clear')
    print("\n  === CONNECT 4 ===\n")
    
    # Print column labels
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print("\n  " + "---" * COLS)
    
    # Print rows from top to bottom
    for row in board:
        print("  |", end="")
        for cell in row:
            print(f"{cell}|", end="")
        print()
    
    # Print bottom border
    print("  " + "---" * COLS)
    print()

# ============================================================================
# INPUT VALIDATION
# ============================================================================

def get_valid_column(board, current_player):
    """Get a valid column input from the current player."""
    while True:
        user_input = input(f"Player {current_player}, enter column (A-G): ").strip().upper()
        
        # Check if input is a valid column label
        if user_input not in COLUMN_LABELS:
            print(f"Invalid input! Please enter a column letter from A to G.")
            continue
        
        # Convert letter to column index
        col_index = COLUMN_LABELS.index(user_input)
        
        # Check if column is full
        if board[0][col_index] != ' ':
            print(f"Column {user_input} is full! Choose another column.")
            continue
        
        return col_index

# ============================================================================
# GAME LOGIC
# ============================================================================

def drop_piece(board, col, symbol):
    """Drop a piece into the specified column. Return the row where it lands."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1  # Should never happen if input validation works

def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) created a winning condition."""
    
    # Check horizontal
    if check_direction(board, row, col, symbol, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, symbol, 1, 0):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, symbol, -1, 1):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, symbol, 1, 1):
        return True
    
    return False

def check_direction(board, row, col, symbol, row_delta, col_delta):
    """
    Check if there are 4 in a row in a specific direction.
    row_delta and col_delta define the direction to check.
    """
    count = 1  # Count the piece we just placed
    
    # Check in the positive direction
    count += count_consecutive(board, row, col, symbol, row_delta, col_delta)
    
    # Check in the negative direction
    count += count_consecutive(board, row, col, symbol, -row_delta, -col_delta)
    
    return count >= WIN_LENGTH

def count_consecutive(board, row, col, symbol, row_delta, col_delta):
    """Count consecutive pieces in one direction."""
    count = 0
    current_row = row + row_delta
    current_col = col + col_delta
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == symbol):
        count += 1
        current_row += row_delta
        current_col += col_delta
    
    return count

def check_draw(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))

# ============================================================================
# MAIN GAME
# ============================================================================

def play_game():
    """Main game loop."""
    # Validate number of players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5!")
        return
    
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\nStarting Connect 4 with {NUM_PLAYERS} players!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("\nPress Enter to begin...")
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Display board
        display_board(board)
        print(f"Current players: {' vs '.join(players)}")
        
        # Get valid move
        col = get_valid_column(board, current_player)
        
        # Drop piece and get row position
        row = drop_piece(board, col, current_player)
        
        # Check for win
        if check_win(board, row, col, current_player):
            display_board(board)
            print(f"🎉 CONGRATULATIONS! Player {current_player} wins! 🎉\n")
            break
        
        # Check for draw
        if check_draw(board):
            display_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    play_game()
