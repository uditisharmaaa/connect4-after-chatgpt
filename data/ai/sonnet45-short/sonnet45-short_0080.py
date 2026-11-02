import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board"""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  " + "   ".join(COLUMNS))
    print(" +" + "---+" * COLS)
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(col_input):
    """Check if column input is valid"""
    return col_input.upper() in COLUMNS

def get_col_index(col_input):
    """Convert column letter to index"""
    return COLUMNS.index(col_input.upper())

def is_column_full(board, col_index):
    """Check if a column is full"""
    return board[0][col_index] != ' '

def drop_piece(board, col_index, player):
    """Drop a piece into the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win"""
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
    r, c = start_row, start_col
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
    r, c = start_row, start_col
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
    return all(board[0][c] != ' ' for c in range(COLS))

def get_player_input(player):
    """Get valid input from the player"""
    while True:
        col_input = input(f"Player {player}, enter column (A-G): ").strip()
        
        if not col_input:
            print("Invalid input! Please enter a column letter.")
            continue
        
        if not is_valid_column(col_input):
            print("Invalid column! Please enter A-G.")
            continue
        
        col_index = get_col_index(col_input)
        if is_column_full(board, col_index):
            print("Column is full! Choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop"""
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\nWelcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"First player (randomly selected): {PLAYERS[current_player_index]}")
    input("\nPress Enter to start...")
    
    while True:
        player = PLAYERS[current_player_index]
        print_board(board)
        
        col_index = get_player_input(player)
        row = drop_piece(board, col_index, player)
        
        if check_win(board, row, col_index, player):
            print_board(board)
            print(f"🎉 Player {player} wins! 🎉")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
