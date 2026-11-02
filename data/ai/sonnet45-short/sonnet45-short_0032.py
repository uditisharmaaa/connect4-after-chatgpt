import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def drop_piece(board, col, symbol):
    """Drop a piece into the specified column. Returns row if successful, -1 if column is full"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def is_valid_column(col_input):
    """Validate that the input is a valid column letter"""
    return col_input.upper() in COLUMN_LABELS

def get_column_index(col_input):
    """Convert column letter to index"""
    return COLUMN_LABELS.index(col_input.upper())

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win"""
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
    """Check if the board is full (draw condition)"""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop"""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Players: {', '.join(players)}")
    print(f"Starting player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        
        # Get valid input
        while True:
            col_input = input(f"Player {current_symbol}, choose a column (A-G): ")
            
            if not col_input:
                print("Please enter a column letter!")
                continue
            
            if not is_valid_column(col_input):
                print(f"Invalid column! Please choose from A-G.")
                continue
            
            col = get_column_index(col_input)
            
            if board[0][col] != ' ':
                print("That column is full! Choose another.")
                continue
            
            break
        
        # Drop the piece
        row = drop_piece(board, col, current_symbol)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
