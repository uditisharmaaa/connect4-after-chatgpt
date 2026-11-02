import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board(rows, cols):
    """Create and initialize the Connect 4 board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, rows, cols):
    """Print the current state of the board with column labels."""
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(65 + i) for i in range(cols)]))
    
    # Print top border
    print("+" + "---+" * cols)
    
    # Print each row
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * cols)

def is_valid_column(col, cols):
    """Check if the column input is valid (a letter within bounds)."""
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(65 + cols - 1)

def get_drop_row(board, col, rows):
    """Get the lowest empty row in the specified column (0-indexed from top)."""
    col_idx = ord(col) - 65
    for row_idx in range(rows - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            return row_idx
    return -1  # Column is full

def place_checker(board, row, col, checker):
    """Place the checker on the board at the specified position."""
    col_idx = ord(col) - 65
    board[row][col_idx] = checker

def check_win(board, rows, cols, row, col, checker):
    """Check if the current move resulted in a win."""
    col_idx = ord(col) - 65
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Current cell is already counted
        # Check in positive direction
        r, c = row + dr, col_idx + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col_idx - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board, rows, cols):
    """Check if the board is full (no empty spaces)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main game loop for Connect 4."""
    # Initialize game
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    clear_screen()
    print_board(board, BOARD_ROWS, BOARD_COLS)
    
    while True:
        checker = checkers[current_player]
        print(f"Player {checker}, please enter a column: ")
        col_input = input().strip().upper()
        
        # Validate input
        if not is_valid_column(col_input, BOARD_COLS):
            print("Invalid column! Please enter a letter from A to " + chr(65 + BOARD_COLS - 1))
            continue
        
        # Check if column has space
        drop_row = get_drop_row(board, col_input, BOARD_ROWS)
        if drop_row == -1:
            print("Column is full! Please choose another column.")
            continue
        
        # Place checker and check for win/draw
        place_checker(board, drop_row, col_input, checker)
        clear_screen()
        print_board(board, BOARD_ROWS, BOARD_COLS)
        
        if check_win(board, BOARD_ROWS, BOARD_COLS, drop_row, col_input, checker):
            print(f"Player {checker} won!")
            break
        
        if is_board_full(board, BOARD_ROWS, BOARD_COLS):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
