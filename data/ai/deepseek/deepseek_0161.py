import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Takes first NUM_PLAYERS symbols

def initialize_board():
    """Create an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    
    print(border)

def is_valid_column(col):
    """Check if the column input is valid (A, B, etc. within bounds)."""
    if len(col) != 1:
        return False
    col_char = col.upper()
    return col_char >= 'A' and col_char <= chr(65 + COLS - 1)

def drop_checker(board, col, checker):
    """Drop the checker into the specified column.
    Returns True if successful, False if column is full."""
    col_idx = ord(col.upper()) - ord('A')
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the given checker has won (4 in a row horizontally, vertically, or diagonally)."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True

    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True

    # Check diagonals (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True

    # Check diagonals (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    print_board(board)
    
    while True:
        player_symbol = PLAYERS[current_player]
        print(f"Player {player_symbol}, please enter a column: ", end='')
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A, B, etc.).")
            continue
        
        if not drop_checker(board, col_input, player_symbol):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
