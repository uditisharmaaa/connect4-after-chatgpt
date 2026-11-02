# Connect 4 Game
# A simple Connect 4 game for 2-5 players

import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board"""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  Connect 4")
    print("=" * 29)
    
    # Print column labels
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(label + "  ", end="")
    print()
    
    # Print rows
    for row in range(ROWS):
        print(row + 1, end=" ")
        for col in range(COLS):
            print(board[row][col] + "  ", end="")
        print()
    
    print("=" * 29)

def is_valid_column(column):
    """Check if the column input is valid"""
    column = column.upper()
    return column in COLUMN_LABELS

def get_column_number(column):
    """Convert column letter to column number"""
    column = column.upper()
    return COLUMN_LABELS.index(column)

def is_column_full(board, col_num):
    """Check if a column is full"""
    return board[0][col_num] != ' '

def drop_piece(board, col_num, player):
    """Drop a piece into the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_num] == ' ':
            board[row][col_num] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the current move wins the game"""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player:
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
        if board[r][c] == player:
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
        if board[r][c] == player:
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

def play_game():
    """Main game loop"""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    print(f"\nStarting player: {PLAYERS[current_player_index]}")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        # Get player input
        while True:
            column = input(f"\nPlayer {current_player}, choose a column (A-G): ")
            
            if not is_valid_column(column):
                print("Invalid column! Please choose A-G.")
                continue
            
            col_num = get_column_number(column)
            
            if is_column_full(board, col_num):
                print("That column is full! Choose another.")
                continue
            
            break
        
        # Drop the piece
        row = drop_piece(board, col_num, current_player)
        
        # Check for win
        if check_win(board, row, col_num, current_player):
            print_board(board)
            print(f"\n*** Player {current_player} WINS! ***\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("\n*** It's a DRAW! ***\n")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Main program
if __name__ == "__main__":
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    input("Press Enter to begin...")
    
    play_game()
    
    print("Thanks for playing!")
