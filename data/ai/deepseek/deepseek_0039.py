import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(COLS)]) + "  "
    print(header)
    
    # Print board rows with separators
    for row in board:
        separator = "+" + ("---+") * COLS
        print(separator)
        print("| " + " | ".join(row) + " |")
    print("+" + ("---+") * COLS)

def get_random_first_player():
    """Randomly select the first player."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col_char = col.upper()
    if not col_char.isalpha():
        return False
    col_idx = ord(col_char) - ord('A')
    return 0 <= col_idx < COLS

def get_column_index(col):
    """Convert column character to index."""
    return ord(col.upper()) - ord('A')

def place_checker(board, col_idx, player):
    """Place the checker in the lowest available row of the column."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player
            return (row_idx, col_idx)
    return None  # Column is full

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down
        (1, -1)   # Diagonal up
    ]
    
    for dr, dc in directions:
        count = 1  # The current position is already the player's checker
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = get_random_first_player()
    print_board(board)
    
    while True:
        player_symbol = PLAYERS[current_player]
        print(f"Player {player_symbol}, please enter a column: ", end="")
        col_input = input().strip()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        
        col_idx = get_column_index(col_input)
        placement = place_checker(board, col_idx, player_symbol)
        
        if placement is None:
            print("Column is full. Please choose another column.")
            continue
        
        row, col = placement
        print_board(board)
        
        if check_win(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
