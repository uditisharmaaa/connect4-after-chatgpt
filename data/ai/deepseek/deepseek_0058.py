import os
import random

# Constants for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Possible player tokens in order
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Initialize an empty board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels."""
    # Print column headers (A, B, C, ...)
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    
    # Print board rows with borders
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    
    print("+---+---+---+---+---+---+---+")

def get_valid_column_input(board, player_token):
    """Prompt the player for a valid column input."""
    columns = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        column = input(f"Player {player_token}, please enter a column: ").upper()
        if not column or column not in columns:
            print("Invalid column. Please enter a valid column letter (A-{}).".format(chr(ord('A') + len(board[0]) - 1)))
            continue
        
        col_index = ord(column) - ord('A')
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col_index, player_token):
    """Place the player's checker in the lowest available row of the specified column."""
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = player_token
            return row, col_index
    return None  # Column is full (should not happen as input is validated)

def check_win(board, row, col, player_token):
    """Check if the last move resulted in a win for the player."""
    # Directions: (row, col) changes for horizontal, vertical, and two diagonals
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
        
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def check_draw(board):
    """Check if the board is full (a draw)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    os.system('clear')
    
    # Initialize game state
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print("Starting Connect 4!")
    print(f"Player {players[current_player_idx]} goes first.")
    print_board(board)
    
    while True:
        current_player = players[current_player_idx]
        col_index = get_valid_column_input(board, current_player)
        row_placed, col_placed = place_checker(board, col_index, current_player)
        
        os.system('clear')
        print_board(board)
        
        if check_win(board, row_placed, col_placed, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Move to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
