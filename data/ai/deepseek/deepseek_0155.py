import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Only use the first NUM_PLAYERS symbols

def initialize_board():
    """Initialize an empty board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print the board
    for row in board:
        print('+---+' * BOARD_COLS)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    
    print('+---+' * BOARD_COLS)

def get_valid_column(board):
    """Prompt the player to enter a valid column and return the column index."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        
        # Check if input is a single letter
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-" + chr(ord('A') + BOARD_COLS - 1) + ").")
            continue
        
        col = ord(col_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= BOARD_COLS:
            print("Column out of bounds. Please try again.")
            continue
        
        # Check if column is not full
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column at the lowest available row."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move caused a win (4 in a row horizontally, vertically, or diagonally)."""
    # Check horizontal
    count = 1
    # Left side
    i = col - 1
    while i >= 0 and board[row][i] == player:
        count += 1
        i -= 1
    # Right side
    i = col + 1
    while i < BOARD_COLS and board[row][i] == player:
        count += 1
        i += 1
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    # Upwards
    i = row - 1
    while i >= 0 and board[i][col] == player:
        count += 1
        i -= 1
    # Downwards
    i = row + 1
    while i < BOARD_ROWS and board[i][col] == player:
        count += 1
        i += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Top-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == player:
        count += 1
        i -= 1
        j -= 1
    # Bottom-right
    i, j = row + 1, col + 1
    while i < BOARD_ROWS and j < BOARD_COLS and board[i][j] == player:
        count += 1
        i += 1
        j += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Top-right
    i, j = row - 1, col + 1
    while i >= 0 and j < BOARD_COLS and board[i][j] == player:
        count += 1
        i -= 1
        j += 1
    # Bottom-left
    i, j = row + 1, col - 1
    while i < BOARD_ROWS and j >= 0 and board[i][j] == player:
        count += 1
        i += 1
        j -= 1
    if count >= 4:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled (draw condition)."""
    return all(cell != ' ' for cell in board[0])

# Initialize the game
board = initialize_board()
current_player = random.choice(PLAYERS)
print_board(board)

# Game loop
while True:
    # Get player's move
    col = get_valid_column(board)
    row = place_checker(board, col, current_player)
    
    # Print updated board
    print_board(board)
    
    # Check for win
    if check_win(board, row, col, current_player):
        print(f"Player {current_player} won!")
        break
    
    # Check for draw
    if is_board_full(board):
        print("Game ended in a draw!")
        break
    
    # Switch player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
