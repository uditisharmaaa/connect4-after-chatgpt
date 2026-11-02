# Connect 4 Game
# By: [Your Name]
# For: Intro CS Class

import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this to 2-5 players

def create_board():
    """Create an empty game board"""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append('.')
        board.append(row)
    return board

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +-+-+-+-+-+-+-+")
    for i in range(ROWS):
        print(str(i + 1) + "|", end="")
        for j in range(COLS):
            print(board[i][j] + "|", end="")
        print()
    print(" +-+-+-+-+-+-+-+")
    print("  A B C D E F G\n")

def get_column_input():
    """Get and validate column input from player"""
    while True:
        col_input = input("Enter column (A-G): ").upper()
        if len(col_input) == 1 and col_input >= 'A' and col_input <= 'G':
            return ord(col_input) - ord('A')  # Convert letter to number 0-6
        else:
            print("Invalid input! Please enter A, B, C, D, E, F, or G.")

def is_column_full(board, col):
    """Check if a column is full"""
    return board[0][col] != '.'

def drop_piece(board, col, symbol):
    """Drop a piece into the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == '.':
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
        if not is_column_full(board, col):
            return False
    return True

def play_game():
    """Main game function"""
    # Setup
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(PLAYER_SYMBOLS[i])
    
    # Pick random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        print_board(board)
        current_symbol = players[current_player_index]
        print(f"Player {current_symbol}'s turn")
        
        # Get valid move
        while True:
            col = get_column_input()
            if is_column_full(board, col):
                print("That column is full! Choose another.")
            else:
                break
        
        # Make move
        row = drop_piece(board, col, current_symbol)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
