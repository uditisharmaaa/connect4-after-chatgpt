import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for up to 5 players

def create_board():
    """Create and initialize a game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = "  " + "   ".join([chr(65 + i) for i in range(COLS)])
    print(header)
    
    # Print each row with borders
    border = "+" + ("---+" * COLS)
    for row in board:
        print(border)
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
    print(border)

def get_random_first_player(num_players):
    """Randomly select the first player."""
    return random.randint(0, num_players - 1)

def is_valid_column(column):
    """Check if the entered column is valid."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return col_char >= 'A' and col_char <= chr(65 + COLS - 1)

def get_next_open_row(board, col):
    """Find the next open row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1  # Column is full

def place_checker(board, row, col, player_symbol):
    """Place the player's checker in the specified position."""
    board[row][col] = player_symbol

def check_win(board, row, col):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    player = board[row][col]
    
    for dr, dc in directions:
        count = 1  # Include the current checker
        # Check in one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        # If 4 in a row, return win
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = get_random_first_player(NUM_PLAYERS)
    
    while True:
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {player_symbol}, please enter a column: ")
        
        # Get and validate column input
        while True:
            col_input = input().strip().upper()
            if not is_valid_column(col_input):
                print("Invalid input. Please enter a valid column (A-" + chr(65 + COLS - 1) + "): ")
                continue
            col = ord(col_input) - ord('A')
            row = get_next_open_row(board, col)
            if row == -1:
                print("Column is full. Please choose another column: ")
                continue
            break
        
        # Place the checker
        place_checker(board, row, col, player_symbol)
        
        # Check for win
        if check_win(board, row, col):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
