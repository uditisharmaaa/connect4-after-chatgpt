import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col >= 'A' and col < chr(65 + COLS)

def get_column_index(col):
    """Convert the column letter to an index."""
    return ord(col.upper()) - 65

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible."""
    col_idx = get_column_index(col)
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the player with the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled with checkers."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        os.system('clear')
        print_board(board)
        
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ")
        col_input = input().strip()
        
        if not is_valid_column(col_input):
            print("Invalid column. Please enter a letter from A to " + chr(64 + COLS))
            input("Press Enter to continue...")
            continue
        
        col = col_input.upper()
        if not place_checker(board, col, checker):
            print("Column is full. You lose your turn.")
            input("Press Enter to continue...")
        else:
            if check_win(board, checker):
                os.system('clear')
                print_board(board)
                print(f"Player {checker} won!")
                break
            if is_board_full(board):
                os.system('clear')
                print_board(board)
                print("It's a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS
        
if __name__ == "__main__":
    play_game()
