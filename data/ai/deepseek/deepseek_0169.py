import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col >= 'A' and col <= chr(ord('A') + COLS - 1)

def get_column_index(col):
    """Convert column letter to 0-based index."""
    return ord(col.upper()) - ord('A')

def drop_checker(board, col, checker):
    """Try to drop a checker into the specified column.
    Returns True if successful, False if the column is full."""
    col_index = get_column_index(col)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    while True:
        os.system('clear')
        print_board(board)
        
        print(f"Player {PLAYERS[current_player]}, please enter a column:")
        col = input().strip()
        
        if not is_valid_column(col):
            print("Invalid input! Please enter a letter from A to G.")
            input("Press Enter to continue...")
            continue
        
        col = col.upper()
        if not drop_checker(board, col, PLAYERS[current_player]):
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
        else:
            if check_win(board, PLAYERS[current_player]):
                os.system('clear')
                print_board(board)
                print(f"Player {PLAYERS[current_player]} won!")
                break
            
            if is_board_full(board):
                os.system('clear')
                print_board(board)
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
