import random
import os

# Constants
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
    print("\n  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(column_input):
    """Check if the column input is valid (A-G)."""
    return column_input.upper() in COLUMN_LABELS

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != ' '

def drop_piece(board, col_index, symbol):
    """Drop a piece into the specified column. Returns the row where it landed."""
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
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))

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

def get_player_move(player_symbol):
    """Get and validate a player's column choice."""
    while True:
        column_input = input(f"Player {player_symbol}, choose a column (A-G): ").strip().upper()
        
        if not is_valid_column(column_input):
            print("Invalid column. Please choose A, B, C, D, E, F, or G.")
            continue
        
        col_index = COLUMN_LABELS.index(column_input)
        
        if is_column_full(board, col_index):
            print("That column is full. Please choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    global board
    
    os.system('clear')
    print("=" * 40)
    print("       WELCOME TO CONNECT 4!")
    print("=" * 40)
    
    # Get number of players
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    
    # Initialize board
    board = create_board()
    
    # Pick random first player
    current_player_index = random.randint(0, num_players - 1)
    
    print(f"\nPlayers: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("\nPress Enter to start...")
    
    # Game loop
    moves = 0
    max_moves = ROWS * COLS
    
    while moves < max_moves:
        os.system('clear')
        print_board(board)
        
        current_symbol = players[current_player_index]
        
        # Get player move
        col_index = get_player_move(current_symbol)
        
        # Drop piece
        row = drop_piece(board, col_index, current_symbol)
        moves += 1
        
        # Check for win
        if check_win(board, row, col_index, current_symbol):
            os.system('clear')
            print_board(board)
            print("=" * 40)
            print(f"   Player {current_symbol} WINS!")
            print("=" * 40)
            return
        
        # Check for draw
        if is_board_full(board):
            os.system('clear')
            print_board(board)
            print("=" * 40)
            print("   GAME ENDS IN A DRAW!")
            print("=" * 40)
            return
        
        # Next player
        current_player_index = (current_player_index + 1) % num_players

def main():
    """Main function to run the game."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("\nThanks for playing Connect 4!")
            break

if __name__ == "__main__":
    main()
