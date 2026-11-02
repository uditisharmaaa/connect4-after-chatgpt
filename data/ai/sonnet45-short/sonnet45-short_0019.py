import os
import random

# Constants
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
    print("\n  " + "   ".join(COLUMN_LABELS))
    print("  " + "---" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("  " + "---" * COLS)
    print()

def is_valid_column(column_letter):
    """Check if the column letter is valid (A-G)."""
    return column_letter.upper() in COLUMN_LABELS

def get_column_index(column_letter):
    """Convert column letter to index (0-6)."""
    return COLUMN_LABELS.index(column_letter.upper())

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != EMPTY

def drop_piece(board, col_index, symbol):
    """Drop a piece into the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            board[row][col_index] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) resulted in a win."""
    
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
    return all(board[0][col] != EMPTY for col in range(COLS))

def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, enter column (A-G): ").strip()
        
        if not move:
            print("Please enter a column letter.")
            continue
        
        if not is_valid_column(move):
            print("Invalid column. Please choose A-G.")
            continue
        
        col_index = get_column_index(move)
        
        if is_column_full(board, col_index):
            print("That column is full. Choose another.")
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
        print_board(board)
        current_symbol = players[current_player_index]
        
        col_index = get_player_move(board, current_symbol)
        row = drop_piece(board, col_index, current_symbol)
        
        if check_win(board, row, col_index, current_symbol):
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
    """Entry point for the game."""
    print("=" * 40)
    print("       WELCOME TO CONNECT 4!")
    print("=" * 40)
    
    while True:
        try:
            num_players = int(input(f"\nEnter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                break
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nPlayers: {', '.join(PLAYER_SYMBOLS[:num_players])}")
    
    play_game(num_players)
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
