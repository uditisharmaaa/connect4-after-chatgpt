import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with columns labeled A, B, C, etc."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print each row with borders
    for row in board:
        border = '+' + ('---+' * COLS)
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print bottom border
    print('+' + ('---+' * COLS))

def get_valid_column(board):
    """Prompt the player for a valid column input."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column out of range. Please enter a letter between A-{chr(65 + COLS - 1)}.")
            continue
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col

def drop_checker(board, col, symbol):
    """Drop a checker into the specified column and return the row where it lands."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1  # Column is full (should not happen if validated)

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down
        (1, -1)   # Diagonal up
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        # If count >= 4, win
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main function to play the Connect 4 game."""
    global current_player
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        row = drop_checker(board, col, PLAYER_SYMBOLS[current_player])
        print_board(board)
        
        if check_win(board, row, col, PLAYER_SYMBOLS[current_player]):
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
