import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    print("\n  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(col_letter):
    """Check if column input is valid."""
    return col_letter.upper() in COLUMN_LABELS

def get_column_index(col_letter):
    """Convert column letter to index."""
    return COLUMN_LABELS.index(col_letter.upper())

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != ' '

def drop_piece(board, col_index, symbol):
    """Drop a piece into the specified column."""
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

def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}): ")
        
        if not is_valid_column(move):
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[COLS-1]}.")
            continue
        
        col_index = get_column_index(move)
        
        if is_column_full(board, col_index):
            print("That column is full! Choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    # Initialize game
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    os.system('clear')
    print("=" * 30)
    print("   CONNECT 4 GAME")
    print("=" * 30)
    print(f"\nNumber of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(players)}")
    print(f"\nFirst player: {players[current_player_index]}")
    input("\nPress Enter to start...")
    
    # Game loop
    while True:
        os.system('clear')
        print_board(board)
        
        current_symbol = players[current_player_index]
        col_index = get_player_move(board, current_symbol)
        row_index = drop_piece(board, col_index, current_symbol)
        
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_symbol):
            print("=" * 30)
            print(f"   PLAYER {current_symbol} WINS!")
            print("=" * 30)
            break
        
        # Check for draw
        if is_board_full(board):
            print("=" * 30)
            print("   IT'S A DRAW!")
            print("=" * 30)
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Entry point of the program."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            break

if __name__ == "__main__":
    main()
