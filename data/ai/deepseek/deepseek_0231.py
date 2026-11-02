import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First NUM_PLAYERS symbols

def clear_screen():
    """Clear the console screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(BOARD_COLS)]) + '  '
    print(header)
    
    # Print top border
    print('+' + ('---+' * BOARD_COLS))
    
    # Print each row
    for row in board:
        print('|' + ('   |' * BOARD_COLS))
        # Print cells with content
        row_str = '|'
        for cell in row:
            row_str += f' {cell} |'
        print(row_str)
        print('|' + ('   |' * BOARD_COLS))
        print('+' + ('---+' * BOARD_COLS))

def get_valid_column():
    """Prompt the current player to enter a column and validate the input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter from A to", chr(ord('A') + BOARD_COLS - 1))
            continue
        col_num = ord(col) - ord('A')
        if col_num < 0 or col_num >= BOARD_COLS:
            print("Column out of range. Please choose a column from A to", chr(ord('A') + BOARD_COLS - 1))
            continue
        return col_num

def drop_checker(board, col, player):
    """Place the player's checker in the specified column if possible.
    Returns True if successful, False otherwise."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and
                board[row][col+1] == player and
                board[row][col+2] == player and
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == player and
                board[row+1][col] == player and
                board[row+2][col] == player and
                board[row+3][col] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and
                board[row+1][col+1] == player and
                board[row+2][col+2] == player and
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and
                board[row-1][col+1] == player and
                board[row-2][col+2] == player and
                board[row-3][col+3] == player):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (no more moves possible)."""
    return all(cell != ' ' for row in board for cell in row)

# Initialize the game
board = create_board()
current_player = random.choice(PLAYERS)
winner = None

# Main game loop
while True:
    clear_screen()
    print_board(board)
    
    # Check for draw
    if is_board_full(board):
        print("The game is a draw!")
        break
    
    # Get valid column input
    col = get_valid_column()
    
    # Try to place the checker
    if not drop_checker(board, col, current_player):
        print("Column is full. You lose your turn.")
    else:
        # Check for win
        if check_win(board, current_player):
            winner = current_player
            break
    
    # Switch player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

# Game over
clear_screen()
print_board(board)
if winner:
    print(f"Player {winner} won!")
else:
    print("The game is a draw!")
