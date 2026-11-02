import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a new empty board with the given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(len(board[0]))]) + '  '
    print(header)
    
    # Print the board
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print(border)

def is_valid_column(col, cols):
    """Check if the given column is valid."""
    return len(col) == 1 and col.isalpha() and ord(col.upper()) - 65 < cols

def get_column_index(col):
    """Convert column letter to index."""
    return ord(col.upper()) - 65

def drop_checker(board, col, checker):
    """Drop the checker in the specified column."""
    col_index = get_column_index(col)
    
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the given checker has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontally
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertically
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonally (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonally (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player]}, please enter a column: ")
        col = input().strip().upper()
        
        if not is_valid_column(col, COLS):
            print("Invalid column. Please try again.")
            continue
        
        if not drop_checker(board, col, PLAYERS[current_player]):
            print("Column is full. Try another column.")
            continue
        
        if check_win(board, PLAYERS[current_player]):
            print_board(board)
            print(f"Player {PLAYERS[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
