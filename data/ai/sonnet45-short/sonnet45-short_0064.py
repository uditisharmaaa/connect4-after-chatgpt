import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  A   B   C   D   E   F   G")
    print("╔═══╦═══╦═══╦═══╦═══╦═══╦═══╗")
    for row in range(ROWS):
        print("║", end="")
        for col in range(COLS):
            print(f" {board[row][col]} ║", end="")
        print()
        if row < ROWS - 1:
            print("╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣")
    print("╚═══╩═══╩═══╩═══╩═══╩═══╩═══╝")
    print("  A   B   C   D   E   F   G\n")

def get_column_input():
    """Get and validate column input from player"""
    while True:
        col_input = input("Enter column (A-G): ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= 'G':
            return ord(col_input) - ord('A')
        print("Invalid input! Please enter a letter from A to G.")

def is_valid_move(board, col):
    """Check if a move is valid (column not full)"""
    return board[0][col] == ' '

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

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
    """Check if the board is completely full (draw)"""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop"""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print("=" * 40)
    print("WELCOME TO CONNECT 4!")
    print("=" * 40)
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_idx]}")
    input("Press Enter to start...")
    
    moves_made = 0
    max_moves = ROWS * COLS
    
    while moves_made < max_moves:
        current_symbol = players[current_player_idx]
        print_board(board)
        print(f"Player {current_symbol}'s turn")
        
        # Get valid move
        while True:
            col = get_column_input()
            if is_valid_move(board, col):
                break
            print("Column is full! Choose another column.")
        
        # Drop piece and check for win
        row = drop_piece(board, col, current_symbol)
        moves_made += 1
        
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print("=" * 40)
            print(f"🎉 PLAYER {current_symbol} WINS! 🎉")
            print("=" * 40)
            return
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("=" * 40)
            print("IT'S A DRAW!")
            print("=" * 40)
            return
        
        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

def main():
    """Main function to run the game"""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
