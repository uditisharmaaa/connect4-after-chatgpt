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
    # Clear the screen before each print
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print board rows with borders
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print bottom border
    print('+---' * COLS + '+')

def is_valid_column(column):
    """Check if the input column is valid."""
    if len(column) != 1:
        return False
    col = ord(column.upper()) - 65
    return 0 <= col < COLS

def get_next_row(board, col):
    """Find the next available row in the specified column."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return -1

def place_checker(board, col, checker):
    """Place the checker in the specified column."""
    row = get_next_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != ' ' for c in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player]}, please enter a column: ")
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid column. Please try again.")
            continue
        
        col = ord(column) - 65
        if not place_checker(board, col, PLAYERS[current_player]):
            print("Column is full. Please try another column.")
            continue
        
        if check_win(board, PLAYERS[current_player]):
            print_board(board)
            print(f"Player {PLAYERS[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
