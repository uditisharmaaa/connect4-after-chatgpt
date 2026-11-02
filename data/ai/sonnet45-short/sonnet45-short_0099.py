import os
import random

# Game Constants
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
    """Display the game board with column labels."""
    os.system('clear')
    print("\n  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("  " + " ".join(row))
    print()

def is_valid_column(col_input):
    """Check if the column input is valid."""
    return col_input.upper() in COLUMN_LABELS

def get_column_index(col_input):
    """Convert column letter to index."""
    return COLUMN_LABELS.index(col_input.upper())

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != EMPTY

def drop_piece(board, col_index, symbol):
    """Drop a piece in the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY:
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
            if count >= 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count >= 4:
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
            if count >= 4:
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
            if count >= 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != EMPTY for col in range(COLS))

def get_player_move(board, player_symbol):
    """Get and validate player move."""
    while True:
        move = input(f"Player {player_symbol}, enter column (A-G): ").strip()
        
        if not move:
            print("Please enter a column!")
            continue
        
        if not is_valid_column(move):
            print("Invalid column! Please enter A-G.")
            continue
        
        col_index = get_column_index(move)
        
        if is_column_full(board, col_index):
            print("That column is full! Choose another.")
            continue
        
        return col_index

def play_game(num_players):
    """Main game loop."""
    board = create_board()
    players = PLAYER_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    print(f"\nStarting player: {players[current_player_index]}")
    input("Press Enter to begin...")
    
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        
        col_index = get_player_move(board, current_symbol)
        row_index = drop_piece(board, col_index, current_symbol)
        
        if check_win(board, row_index, col_index, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players

def main():
    """Initialize and start the game."""
    print("=" * 30)
    print("   CONNECT 4")
    print("=" * 30)
    
    while True:
        try:
            num_players = int(input(f"\nEnter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                break
            print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nPlayers: {', '.join(PLAYER_SYMBOLS[:num_players])}")
    play_game(num_players)

if __name__ == "__main__":
    main()
