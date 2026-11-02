import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Only take needed players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def initialize_board():
    """Initialize an empty game board with NUM_ROWS rows and NUM_COLS columns."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the game board with column headers and borders."""
    # Print column headers
    print('   ' + '   '.join([chr(65 + i) for i in range(NUM_COLS)]))
    
    # Print top border
    print('+' + ('---+' * NUM_COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + ('---+' * NUM_COLS))

def get_valid_move(current_player):
    """Get a valid column input from the current player."""
    while True:
        move = input(f"Player {current_player}, please enter a column: ").upper()
        if len(move) != 1 or move < 'A' or move >= chr(65 + NUM_COLS):
            print(f"Invalid column. Please choose from A to {chr(64 + NUM_COLS)}.")
            continue
        return ord(move) - 65  # Convert to column index (0-based)

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible.
    Returns True if successful, False if column is full."""
    for row in reversed(board):  # Start from bottom row
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win.
    Checks horizontal, vertical, and both diagonals for 4 in a row."""
    # Check horizontal
    count = 1
    # left
    i = col - 1
    while i >= 0 and board[row][i] == checker:
        count += 1
        i -= 1
    # right
    i = col + 1
    while i < NUM_COLS and board[row][i] == checker:
        count += 1
        i += 1
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    # up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # down (no need, since you place from bottom)
    i = row + 1
    while i < NUM_ROWS and board[i][col] == checker:
        count += 1
        i += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # top-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # bottom-right
    i, j = row + 1, col + 1
    while i < NUM_ROWS and j < NUM_COLS and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # top-right
    i, j = row - 1, col + 1
    while i >= 0 and j < NUM_COLS and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # bottom-left
    i, j = row + 1, col - 1
    while i < NUM_ROWS and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= 4:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full (a draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    game_over = False
    
    while not game_over:
        clear_screen()
        print_board(board)
        
        col = get_valid_move(current_player)
        if not place_checker(board, col, current_player):
            print(f"Column {chr(65 + col)} is full. Player {current_player} loses turn.")
            # Switch player if column is full
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
            continue
        
        # Find the row where the checker was placed
        for row_idx in range(NUM_ROWS):
            if board[row_idx][col] == current_player:
                last_row = row_idx
                break
        
        if check_win(board, last_row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            game_over = True
        else:
            # Switch players
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
