import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print board rows with borders
    border = '+' + ('---+' * COLS)
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def is_valid_column(col):
    """Check if the input column is valid (A, B, ..., G)."""
    return len(col) == 1 and 'A' <= col <= chr(ord('A') + COLS - 1)

def place_checker(board, col, checker):
    """
    Place the checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    col_idx = ord(col) - ord('A')
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx
    return -1

def check_win(board, row, col):
    """
    Check if the last move resulted in a win.
    Returns True if the player has 4 checkers in a row.
    """
    checker = board[row][col]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, diagonal down, diagonal up
    
    for dr, dc in directions:
        count = 1  # the current checker
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    while True:
        os.system('clear')
        print_board(board)
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ")
        
        while True:
            col = input().strip().upper()
            if not is_valid_column(col):
                print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
                continue
            
            col_idx = ord(col) - ord('A')
            if board[0][col_idx] != ' ':
                print("Column is full. Please choose another column.")
                continue
            
            row = place_checker(board, col, checker)
            if row == -1:
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        if check_win(board, row, col_idx):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
