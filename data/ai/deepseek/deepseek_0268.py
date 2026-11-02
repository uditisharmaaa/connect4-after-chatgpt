import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]

def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    header = "  " + "   ".join([chr(65 + i) for i in range(COLS)]) + "  "
    print(header)
    
    # Print top border
    border = "+" + ("---+" * COLS)
    print(border)
    
    # Print each row
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print(border)

def get_valid_column(current_player):
    """Prompt the player for a column and validate the input."""
    while True:
        try:
            col = input(f"Player {current_player}, please enter a column: ").upper()
            if len(col) != 1 or not col.isalpha():
                print("Invalid input. Please enter a single letter (A-G).")
                continue
            
            col_idx = ord(col) - ord('A')
            if col_idx < 0 or col_idx >= COLS:
                print(f"Column out of range. Please enter a letter between A-{chr(65 + COLS - 1)}.")
                continue
                
            return col_idx
        except EOFError:
            print("Invalid input. Please try again.")

def place_checker(board, col_idx, current_player):
    """Place the checker in the specified column if possible.
    Returns the row where the checker was placed, or None if the column is full."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = current_player
            return row_idx
    return None

def check_win(board, row_idx, col_idx, current_player):
    """Check if the current move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down
        (1, -1)    # diagonal up
    ]
    
    for dr, dc in directions:
        count = 1  # the current cell
        # Search in the positive direction
        r, c = row_idx + dr, col_idx + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == current_player:
            count += 1
            r += dr
            c += dc
        # Search in the negative direction
        r, c = row_idx - dr, col_idx - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == current_player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    current_player = PLAYER_SYMBOLS[current_player_idx]
    
    print_board(board)
    
    while True:
        # Get valid column input
        col_idx = get_valid_column(current_player)
        
        # Place the checker
        row_idx = place_checker(board, col_idx, current_player)
        if row_idx is None:
            print("Column is full. Turn lost.")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            current_player = PLAYER_SYMBOLS[current_player_idx]
            continue
        
        print_board(board)
        
        # Check for win
        if check_win(board, row_idx, col_idx, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player_idx = (current_player_idx + 1) % PLAYERS
        current_player = PLAYER_SYMBOLS[current_player_idx]

if __name__ == "__main__":
    play_game()
