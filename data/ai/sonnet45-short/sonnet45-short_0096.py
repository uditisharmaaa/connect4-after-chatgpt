import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this to 2-5 players
COLUMN_LABELS = 'ABCDEFG'

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print('\n  ' + '   '.join(COLUMN_LABELS))
    print(' +' + '---+' * COLS)
    
    for row in board:
        print(' | ' + ' | '.join(row) + ' |')
        print(' +' + '---+' * COLS)
    print()

def is_valid_column(col_letter):
    """Check if the column input is valid."""
    return col_letter.upper() in COLUMN_LABELS

def get_column_index(col_letter):
    """Convert column letter to index."""
    return COLUMN_LABELS.index(col_letter.upper())

def is_column_full(board, col):
    """Check if a column is full."""
    return board[0][col] != ' '

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column."""
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

def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").strip()
        
        if not move:
            print("Please enter a column letter.")
            continue
        
        if not is_valid_column(move):
            print(f"Invalid column. Please choose A-G.")
            continue
        
        col = get_column_index(move)
        
        if is_column_full(board, col):
            print("That column is full. Choose another.")
            continue
        
        return col

def play_game():
    """Main game loop."""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!\n")
    input("Press Enter to start...")
    
    while True:
        print_board(board)
        current_symbol = players[current_player_index]
        
        col = get_player_move(board, current_symbol)
        row = drop_piece(board, col, current_symbol)
        
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Run the game with option to play again."""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
