import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print top border
    print("+" + "---+" * COLS)
    
    # Print each row
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * COLS)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    """Convert column letter to index (0-based)."""
    return ord(col.upper()) - 65

def find_empty_row(board, col):
    """Find the lowest empty row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    col_idx = get_column_index(col)
    row = find_empty_row(board, col_idx)
    if row == -1:
        return False  # Column is full
    board[row][col_idx] = player
    return True

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board full)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_letter = col_input[0]
        if not place_checker(board, col_letter, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
