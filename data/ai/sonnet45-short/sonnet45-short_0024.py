import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  Connect 4  \n")
    
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("  " + "---" * COLS)
    
    # Print rows (top to bottom for visual clarity)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("  " + "---" * COLS)
    print()

def get_column_input(player_token):
    """Get and validate column input from player"""
    while True:
        user_input = input(f"Player {player_token}, choose a column (A-G): ").upper().strip()
        
        if len(user_input) != 1:
            print("Please enter a single letter.")
            continue
            
        if user_input not in COLUMN_LABELS:
            print(f"Invalid column. Choose from {', '.join(COLUMN_LABELS)}.")
            continue
            
        return COLUMN_LABELS.index(user_input)

def drop_token(board, col, token):
    """Drop a token in the specified column. Returns row if successful, -1 if column full"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return row
    return -1

def check_win(board, row, col, token):
    """Check if the last move created a win"""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == token:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == token:
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
        if board[r][c] == token:
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
        if board[r][c] == token:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop"""
    board = create_board()
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"Starting Connect 4 with {NUM_PLAYERS} players!")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    while True:
        current_token = players[current_player_index]
        print_board(board)
        
        # Get valid column input
        col = get_column_input(current_token)
        
        # Drop token
        row = drop_token(board, col, current_token)
        
        if row == -1:
            print("That column is full! Choose another.")
            input("Press Enter to continue...")
            continue
        
        # Check for win
        if check_win(board, row, col, current_token):
            print_board(board)
            print(f"🎉 Player {current_token} wins! 🎉")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main program entry point"""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("Thanks for playing Connect 4!")
            break

if __name__ == "__main__":
    main()
