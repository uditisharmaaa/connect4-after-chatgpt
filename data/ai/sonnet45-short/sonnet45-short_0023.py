import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print("\n  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(board, col):
    """Check if a column is valid and not full."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def get_next_row(board, col):
    """Find the next available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def drop_piece(board, col, symbol):
    """Drop a piece into the specified column."""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = symbol
        return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
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

def get_column_input():
    """Get and validate column input from the player."""
    while True:
        user_input = input("Enter column (A-G): ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input! Please enter a single letter.")
            continue
        
        if user_input not in COLUMN_LABELS:
            print(f"Invalid column! Please choose from {', '.join(COLUMN_LABELS)}.")
            continue
        
        return COLUMN_LABELS.index(user_input)

def play_game():
    """Main game loop."""
    # Validate number of players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5!")
        return
    
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("=" * 40)
    print("WELCOME TO CONNECT 4!")
    print("=" * 40)
    print(f"\nNumber of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(players)}")
    print(f"\nFirst player (randomly selected): {players[current_player_index]}")
    input("\nPress Enter to start the game...")
    
    # Game loop
    moves = 0
    max_moves = ROWS * COLS
    
    while moves < max_moves:
        os.system('clear')
        
        current_symbol = players[current_player_index]
        
        print("=" * 40)
        print(f"CONNECT 4 - Player {current_symbol}'s Turn")
        print("=" * 40)
        print_board(board)
        
        # Get valid column input
        while True:
            col = get_column_input()
            
            if is_valid_column(board, col):
                break
            else:
                print(f"Column {COLUMN_LABELS[col]} is full! Choose another column.")
        
        # Drop the piece
        row = drop_piece(board, col, current_symbol)
        moves += 1
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            os.system('clear')
            print("=" * 40)
            print("GAME OVER!")
            print("=" * 40)
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! Congratulations! 🎉\n")
            return
        
        # Check for draw
        if is_board_full(board):
            os.system('clear')
            print("=" * 40)
            print("GAME OVER!")
            print("=" * 40)
            print_board(board)
            print("It's a draw! The board is full.\n")
            return
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main function to run the game with replay option."""
    while True:
        play_game()
        
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("\nThanks for playing Connect 4! Goodbye!")
            break

if __name__ == "__main__":
    main()
