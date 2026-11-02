import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the top border
    print('+' + '---+' * COLS)
    
    # Print each row with borders
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def get_player_markers(num_players):
    """Return the list of player markers in order."""
    markers = ['X', 'O', 'V', 'H', 'M']
    return markers[:num_players]

def is_valid_column(col):
    """Check if the column input is valid (a letter within the column range)."""
    if len(col) != 1 or not col.isalpha():
        return False
    col_index = ord(col.upper()) - ord('A')
    return 0 <= col_index < COLS

def place_checker(board, col, marker):
    """Place the marker in the specified column and return the row where it was placed.
    Returns -1 if the column is full."""
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = marker
            return row
    return -1

def check_win(board, row, col, marker):
    """Check if the current move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(max(0, col - 3), min(COLS, col + 4)):
        if board[row][c] == marker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(max(0, row - 3), min(ROWS, row + 4)):
        if board[r][col] == marker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    for r, c in zip(range(row - 3, row + 4), range(col - 3, col + 4)):
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == marker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    for r, c in zip(range(row + 3, row - 4, -1), range(col - 3, col + 4)):
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == marker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

def is_draw(board):
    """Check if the game is a draw (all cells are filled)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    markers = get_player_markers(PLAYERS)
    current_player = random.randint(0, PLAYERS - 1)
    
    print(f"Player {markers[current_player]} starts first!")
    
    while True:
        print_board(board)
        marker = markers[current_player]
        
        while True:
            col = input(f"Player {marker}, please enter a column: ").strip().upper()
            if is_valid_column(col):
                row = place_checker(board, col, marker)
                if row != -1:
                    break
                print("Column is full! Try another one.")
            else:
                print(f"Invalid column! Please enter a letter from A to {chr(65 + COLS - 1)}.")
        
        if check_win(board, row, ord(col) - ord('A'), marker):
            print_board(board)
            print(f"Player {marker} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
