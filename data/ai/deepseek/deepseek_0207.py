import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]  # Adjust based on NUM_PLAYERS
WIN_CONDITION = 4

def initialize_board():
    """Initialize an empty board with whitespaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(COLS)]) + "  "
    print(header)
    
    # Print the board rows with separators
    separator = "+" + ("---+" * COLS)
    for row in board:
        print(separator)
        inner_row = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(inner_row)
    print(separator)

def get_valid_column(board):
    """Prompt the current player for a column and validate the input."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(ord('A') + COLS - 1)}.")
            continue
        if board[0][col] != " ":
            print("That column is full. Please choose another column.")
            continue
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return (row, col)
    return None  # Column is full (shouldn't happen if validated)

def check_win(board, row, col, player):
    """Check if the current move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Start with the current checker
        
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
        
        if count >= WIN_CONDITION:
            return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game loop."""
    global current_player
    board = initialize_board()
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        row, col = place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

# Randomly choose the first player
current_player = random.choice(PLAYERS)

# Start the game
if __name__ == "__main__":
    play_game()
