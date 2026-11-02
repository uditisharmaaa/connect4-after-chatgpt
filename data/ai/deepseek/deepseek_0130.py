import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Possible player tokens in order
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Create and return an empty board with specified dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))]))
    
    # Print the board rows with borders
    border = "+" + ("---+" * len(board[0]))
    for row in board:
        print(border)
        print("| " + " | ".join(row) + " |")
    print(border)

def get_valid_column(board):
    """
    Prompt the current player for a column input and validate it.
    Returns the valid column index.
    """
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1:
            print("Please enter a single letter.")
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= len(board[0]):
            print(f"Column must be between A and {chr(ord('A') + len(board[0]) - 1)}.")
            continue
        
        if board[0][col] != " ":
            print("That column is full. Please choose another.")
            continue
        
        return col

def place_token(board, col, token):
    """
    Place the player's token in the specified column at the lowest empty row.
    Returns the row where the token was placed.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = token
            return row
    return -1  # Shouldn't happen if column was validated

def check_win(board, row, col):
    """Check if placing a token at (row, col) resulted in a win."""
    token = board[row][col]
    
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # The current token is already counted
        
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled with tokens."""
    return all(cell != " " for cell in board[0])

def play_game():
    """Main function to play the Connect 4 game."""
    global current_player
    
    # Initialize game
    board = initialize_board(ROWS, COLS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        row = place_token(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

# Start the game
if __name__ == "__main__":
    play_game()
