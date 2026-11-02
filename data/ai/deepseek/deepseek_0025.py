import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Players' checkers
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print row content with borders
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def is_valid_column(column):
    """Check if the column input is valid (letter A-G)."""
    if len(column) != 1 or not column.isalpha():
        return False
    return 'A' <= column.upper() <= chr(65 + COLS - 1)

def get_column_index(column):
    """Convert column letter to 0-based index."""
    return ord(column.upper()) - ord('A')

def is_column_full(board, col_index):
    """Check if the specified column is full."""
    return board[0][col_index] != ' '

def place_checker(board, col_index, checker):
    """Place the checker in the lowest available row of the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1  # Column is full (should have been checked before)

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1)    # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (no empty spaces)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        os.system('clear')
        print_board(board)
        
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ")
        column = input().strip()
        
        if not is_valid_column(column):
            continue
        
        col_index = get_column_index(column)
        if is_column_full(board, col_index):
            current_player = (current_player + 1) % NUM_PLAYERS  # Skip turn
            continue
        
        row = place_checker(board, col_index, checker)
        
        if check_win(board, row, col_index, checker):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_board_full(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
