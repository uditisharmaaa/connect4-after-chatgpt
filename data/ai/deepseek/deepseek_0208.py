import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with whitespaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with labeled columns."""
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)])
    print(header)

    # Print the board rows with borders
    for row in board:
        line = '+'.join(['---'] * COLS)
        print(f'+{line}+')
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    
    # Print the bottom border
    line = '+'.join(['---'] * COLS)
    print(f'+{line}+')

def get_valid_column(board):
    """Prompt the current player for a column until a valid one is provided."""
    columns = [chr(ord('A') + i) for i in range(COLS)]
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if col not in columns:
            print(f"Invalid column. Please choose from {', '.join(columns)}.")
            continue
        
        col_idx = ord(col) - ord('A')
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_idx

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row

def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board full)."""
    return all(cell != ' ' for cell in board[0])

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

# Initialize the game
board = initialize_board()
current_player = random.randint(0, NUM_PLAYERS - 1)
players = PLAYER_CHECKERS[:NUM_PLAYERS]

clear_screen()
print_board(board)

# Main game loop
while True:
    col = get_valid_column(board)
    row = place_checker(board, col, players[current_player])
    
    clear_screen()
    print_board(board)
    
    if check_win(board, row, col, players[current_player]):
        print(f"Player {players[current_player]} won!")
        break
    
    if is_draw(board):
        print("Game is a draw!")
        break
    
    # Switch to the next player
    current_player = (current_player + 1) % NUM_PLAYERS
