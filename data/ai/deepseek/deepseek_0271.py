import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print the board
    for row in board:
        print('+---+' * COLS)
        line = '|'
        for cell in row:
            line += ' ' + cell + ' |'
        print(line)
    print('+---+' * COLS)

def is_valid_column(col):
    """Check if the column is valid."""
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(ord('A') + COLS - 1)

def get_column_index(col):
    """Convert column letter to zero-based index."""
    return ord(col.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Place the checker in the specified column.
    Returns the row index where the checker was placed, or -1 if column is full.
    """
    col_idx = get_column_index(col)
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx
    return -1

def check_win(board, row, col, checker):
    """
    Check if the last move resulted in a win.
    Returns True if the current player has won, False otherwise.
    """
    # Directions (row, col): horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for dr, dc in directions:
        count = 1  # Already have one checker at (row, col)
        
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        col = input().strip().upper()
        
        if not is_valid_column(col):
            print("Invalid column. Please enter a letter from A to", chr(ord('A') + COLS - 1))
            input("Press Enter to continue...")
            continue
        
        col_idx = get_column_index(col)
        if board[0][col_idx] != ' ':
            print("Column is full. You lose your turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        row_idx = place_checker(board, col, checker)
        if check_win(board, row_idx, col_idx, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
