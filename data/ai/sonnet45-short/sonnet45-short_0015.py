import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2-5 for different numbers of players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print("\n  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(board, col):
    """Check if a column is valid and has space."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, enter column (A-G): ").strip().upper()
        
        if len(move) != 1:
            print("Invalid input! Please enter a single column letter.")
            continue
        
        if move not in COLUMN_LABELS:
            print(f"Invalid column! Please choose from {', '.join(COLUMN_LABELS)}.")
            continue
        
        col_index = COLUMN_LABELS.index(move)
        
        if not is_valid_column(board, col_index):
            print("That column is full! Choose another column.")
            continue
        
        return col_index

def drop_piece(board, col, symbol):
    """Drop a piece into the specified column and return the row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
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
    """Check if the board is completely full."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    # Validate number of players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5!")
        return
    
    # Set up players
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Initialize game
    board = create_board()
    
    # Pick random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\nWelcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!\n")
    input("Press Enter to start...")
    
    # Game loop
    moves_made = 0
    while True:
        current_symbol = players[current_player_index]
        
        # Display board
        print_board(board)
        
        # Get player move
        col = get_player_move(board, current_symbol)
        
        # Drop piece
        row = drop_piece(board, col, current_symbol)
        moves_made += 1
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! Congratulations! 🎉\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Entry point of the program."""
    while True:
        play_game()
        
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
