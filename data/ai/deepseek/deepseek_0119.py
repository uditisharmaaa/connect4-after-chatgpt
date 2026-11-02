import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with dimensions ROWS x COLS."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def is_valid_column(column):
    """Check if the input column is valid."""
    if len(column) != 1:
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < COLS

def get_valid_column(current_player):
    """Prompt the player for a valid column input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if is_valid_column(col):
            return ord(col) - ord('A')
        print("Invalid column. Please try again.")

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
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
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        col = get_valid_column(current_player)
        if not place_checker(board, col, current_player):
            print("Column is full. Turn lost.")
            continue
        
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        idx = PLAYERS.index(current_player)
        current_player = PLAYERS[(idx + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
