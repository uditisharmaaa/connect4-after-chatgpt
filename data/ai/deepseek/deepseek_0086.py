import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Clear the screen and print the game board."""
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    # Print board rows
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col.isalpha() and ord(col) >= 65 and ord(col) < 65 + BOARD_COLS

def get_column_index(col):
    """Convert column letter to column index."""
    return ord(col.upper()) - 65

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the column."""
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print(f"Player {current_player} starts the game.")
    print_board(board)
    
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip()
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_idx = get_column_index(col_input)
        
        if not place_checker(board, col_idx, current_player):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        row_idx = next(r for r in range(BOARD_ROWS) if board[r][col_idx] == current_player)
        if check_win(board, row_idx, col_idx, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("Game ended in a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
