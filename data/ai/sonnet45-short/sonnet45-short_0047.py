import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print('\n  Connect 4\n')
    
    # Print column labels
    print('  ', end='')
    for label in COLUMN_LABELS:
        print(label, end=' ')
    print()
    
    # Print top border
    print(' +' + '-' * (COLS * 2 - 1) + '+')
    
    # Print board rows (top to bottom)
    for row in board:
        print(' |', end='')
        for cell in row:
            print(cell + '|', end='')
        print()
    
    # Print bottom border
    print(' +' + '-' * (COLS * 2 - 1) + '+')
    
    # Print column labels again at bottom
    print('  ', end='')
    for label in COLUMN_LABELS:
        print(label, end=' ')
    print('\n')

def is_valid_move(board, col):
    """Check if a move is valid (column not full)."""
    return 0 <= col < COLS and board[0][col] == ' '

def make_move(board, col, symbol):
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
    """Check if the board is completely full (draw)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_input(player_symbol):
    """Get and validate player input."""
    while True:
        user_input = input(f"Player {player_symbol}, enter column (A-G): ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input! Please enter a single letter A-G.")
            continue
        
        if user_input not in COLUMN_LABELS:
            print("Invalid column! Please enter a letter between A and G.")
            continue
        
        col_index = COLUMN_LABELS.index(user_input)
        return col_index

def play_game():
    """Main game loop."""
    # Validate number of players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5")
        return
    
    # Set up players
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Initialize board
    board = create_board()
    
    # Pick random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Randomly selected Player {players[current_player_index]} to go first!\n")
    input("Press Enter to start the game...")
    
    # Game loop
    moves_made = 0
    while True:
        current_symbol = players[current_player_index]
        
        print_board(board)
        
        # Get valid move
        while True:
            col = get_player_input(current_symbol)
            
            if is_valid_move(board, col):
                break
            else:
                print("That column is full! Choose another column.")
        
        # Make move
        row = make_move(board, col, current_symbol)
        moves_made += 1
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"🎉 Congratulations! Player {current_symbol} wins! 🎉\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main function to run the game."""
    while True:
        play_game()
        
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y' and play_again != 'yes':
            print("Thanks for playing Connect 4!")
            break

if __name__ == "__main__":
    main()
