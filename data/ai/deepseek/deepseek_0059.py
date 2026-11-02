import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(NUM_COLS)]))
    
    # Print the board
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+---' * NUM_COLS + '+')

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col_char = col.upper()
    return col_char.isalpha() and 'A' <= col_char <= chr(65 + NUM_COLS - 1)

def get_column_index(col_char):
    """Convert the column character to a 0-based index."""
    return ord(col_char.upper()) - 65

def is_column_full(board, col_idx):
    """Check if the specified column is full."""
    return board[0][col_idx] != ' '

def drop_checker(board, col_idx, checker):
    """Drop a checker into the specified column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row
    return -1  # Column is full (should not happen if validated)

def check_win(board, row, col):
    """Check if the last move resulted in a win."""
    checker = board[row][col]
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            r, c = row + step * dr, col + step * dc
            while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                count += 1
                r += step * dr
                c += step * dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (board full)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col_input = input().strip()
        
        # Validate input
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + NUM_COLS - 1)))
            continue
        
        col_idx = get_column_index(col_input)
        
        # Check if column is full
        if is_column_full(board, col_idx):
            print("Column is full. Please choose another column.")
            continue
        
        # Place the checker
        row = drop_checker(board, col_idx, current_player)
        
        # Check for win
        if check_win(board, row, col_idx):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch players
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
