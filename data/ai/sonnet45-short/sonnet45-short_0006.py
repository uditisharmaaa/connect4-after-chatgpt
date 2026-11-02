# Connect 4 Game
# A simple Connect 4 game for 2-5 players

import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board"""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +" + "-" * 14 + "+")
    for row in range(ROWS):
        print(str(row + 1) + "|", end="")
        for col in range(COLS):
            print(board[row][col] + " ", end="")
        print("|")
    print(" +" + "-" * 14 "+")
    print("  A B C D E F G\n")

def is_valid_move(board, col):
    """Check if a column has space for another piece"""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def drop_piece(board, col, symbol):
    """Drop a piece into the specified column"""
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
    r = start_row
    c = start_col
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
    r = start_row
    c = start_col
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
    """Check if the board is completely full"""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_move(board, player_symbol):
    """Get and validate player input"""
    while True:
        move = input(f"Player {player_symbol}, enter column (A-G): ").upper().strip()
        
        if len(move) != 1:
            print("Please enter a single letter!")
            continue
        
        if move < 'A' or move > 'G':
            print("Please enter a letter between A and G!")
            continue
        
        col = ord(move) - ord('A')
        
        if not is_valid_move(board, col):
            print("That column is full! Choose another.")
            continue
        
        return col

def play_game():
    """Main game loop"""
    # Setup
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        print_board(board)
        
        # Get move
        col = get_player_move(board, current_symbol)
        
        # Drop piece
        row = drop_piece(board, col, current_symbol)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
