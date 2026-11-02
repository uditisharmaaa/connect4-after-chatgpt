import random
import os

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
    print("\n  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("  " + " ".join(row))
    print()

def is_valid_column(col_input):
    """Check if the column input is valid (A-G)."""
    return col_input.upper() in COLUMN_LABELS

def column_letter_to_index(col_letter):
    """Convert column letter to array index."""
    return COLUMN_LABELS.index(col_letter.upper())

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != EMPTY

def drop_piece(board, col_index, symbol):
    """Drop a piece in the specified column. Returns the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            board[row][col_index] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) created a win for symbol."""
    
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
    
    # Check diagonal (top-left to bottom-right)
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
    
    # Check diagonal (bottom-left to top-right)
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
        if not is_column_full(board, col):
            return False
    return True

def get_number_of_players():
    """Prompt user for number of players and validate input."""
    while True:
        try:
            num_players = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                return num_players
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_player_move(board, player_symbol):
    """Get and validate player's column choice."""
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").strip()
        
        if not move:
            print("Please enter a column letter.")
            continue
        
        if not is_valid_column(move):
            print("Invalid column. Please choose A-G.")
            continue
        
        col_index = column_letter_to_index(move)
        
        if is_column_full(board, col_index):
            print("That column is full. Choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    os.system('clear')
    
    print("=" * 40)
    print("        WELCOME TO CONNECT 4!")
    print("=" * 40)
    print("\nConnect 4 pieces in a row to win!")
    print("(horizontally, vertically, or diagonally)\n")
    
    # Get number of players
    num_players = get_number_of_players()
    players = PLAYER_SYMBOLS[:num_players]
    
    # Randomly select first player
    current_player_index = random.randint(0, num_players - 1)
    
    print(f"\nPlayers: {', '.join(players)}")
    print(f"First player (randomly selected): {players[current_player_index]}")
    input("\nPress Enter to start the game...")
    
    # Initialize board
    board = create_board()
    game_over = False
    
    # Main game loop
    while not game_over:
        os.system('clear')
        
        current_symbol = players[current_player_index]
        
        print_board(board)
        
        # Get player move
        col_index = get_player_move(board, current_symbol)
        
        # Drop piece and get row position
        row = drop_piece(board, col_index, current_symbol)
        
        # Clear screen and show updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, current_symbol):
            print("=" * 40)
            print(f"   PLAYER {current_symbol} WINS!")
            print("=" * 40)
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("=" * 40)
            print("   GAME OVER - IT'S A DRAW!")
            print("=" * 40)
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % num_players
    
    # Ask to play again
    play_again = input("\nPlay again? (y/n): ").strip().lower()
    if play_again == 'y':
        play_game()
    else:
        print("\nThanks for playing!")

# Run the game
if __name__ == "__main__":
    play_game()
