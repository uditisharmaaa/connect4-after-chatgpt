import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers (A, B, C, ...)
    headers = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print each row with borders
    row_separator = '+' + ('---+' * NUM_COLS)
    for row in board:
        print(row_separator)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(row_separator)

def is_valid_column(col):
    """Check if the column input is valid (A, B, ..., up to number of columns)."""
    if len(col) != 1:
        return False
    col_upper = col.upper()
    return col_upper >= 'A' and col_upper <= chr(ord('A') + NUM_COLS - 1)

def get_column_index(col):
    """Convert column letter to its corresponding index."""
    return ord(col.upper()) - ord('A')

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible.
    Returns True if placement was successful, False otherwise."""
    col_idx = get_column_index(col)
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False  # Column is full

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current position is already the checker
        
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        col_input = input().strip()
        
        # Validate input
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column (A-" + chr(ord('A') + NUM_COLS - 1) + ").")
            continue
        
        col = col_input.upper()
        col_idx = get_column_index(col)
        
        # Try to place the checker
        if not place_checker(board, col, current_player):
            print(f"Column {col} is full. Player {current_player} loses turn.")
        else:
            # Check if the current player won
            for row_idx in range(NUM_ROWS):
                if board[row_idx][col_idx] == current_player:
                    if check_win(board, row_idx, col_idx, current_player):
                        print_board(board)
                        print(f"Player {current_player} won!")
                        return
                    break
        
        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            return
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
