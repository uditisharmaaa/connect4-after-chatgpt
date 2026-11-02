import os
import random
import sys

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Possible checker symbols for players
CHECKER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + ('---+' * COLS))

def get_valid_column():
    """Prompt the current player for a column and validate input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        col_index = ord(col) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return (row, col)
    return None  # Column was full (shouldn't happen due to validation)

def check_win(board, row, col, player):
    """Check if the last move resulted in a win for the player."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for dr, dc in directions:
        count = 1  # the current position is already a match
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
            
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
            
        if count >= 4:
            return True
            
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def main():
    global board, current_player
    
    # Initialize the board
    board = initialize_board()
    
    # Select random starting player
    players = CHECKER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    # Main game loop
    while True:
        print_board(board)
        
        # Get valid column from player
        col = get_valid_column()
        
        # Place checker and get its position
        pos = place_checker(col, current_player)
        
        # Check for win
        if check_win(board, pos[0], pos[1], current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
            
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
            
        # Switch player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
