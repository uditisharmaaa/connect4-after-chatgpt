import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column letters (A, B, C, ...)
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print the top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print each row with borders
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row separator
        print('+' + ('---+' * COLS))

def is_valid_column(column):
    """Check if column input is valid (uppercase letter within board bounds)."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return 'A' <= col_char <= chr(ord('A') + COLS - 1)

def get_next_open_row(board, col):
    """Find the lowest empty row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1  # Column is full

def drop_checker(board, row, col, checker):
    """Place the checker at the specified position on the board."""
    board[row][col] = checker

def check_win(board, checker):
    """Check if the current player has won with their last move."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check positive diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check negative diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    clear_screen()
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        col = ord(col_input) - ord('A')
        row = get_next_open_row(board, col)
        
        if row == -1:
            print("Column is full. Please choose another column.")
            continue
        
        drop_checker(board, row, col, current_player)
        clear_screen()
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
