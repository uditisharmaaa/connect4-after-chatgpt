import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Initialize an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with columns labeled A through Z."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print the column headers
    headers = [chr(ord('A') + i) for i in range(COLS)]
    print('  ' + '   '.join(headers))
    
    # Print each row with borders
    border = '+' + ('---+' * COLS)
    print(border)
    for row in board:
        row_str = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(row_str)
        print(border)

def get_valid_column(board):
    """
    Prompt the current player for a column and validate the input.
    Returns the valid column index or None if column is full.
    """
    while True:
        try:
            col_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if not col_input or len(col_input) != 1:
                print("Please enter a single letter.")
                continue
            
            col = ord(col_input) - ord('A')
            if col < 0 or col >= COLS:
                print(f"Column must be between A and {chr(ord('A') + COLS - 1)}.")
                continue
            
            # Check if the column has space
            if board[0][col] != ' ':
                print("Column is full. Please choose another column.")
                return None
            return col
        except:
            print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return None

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current piece counts as 1
        
        # Search in both directions
        for direction in [1, -1]:
            r, c = row + dr*direction, col + dc*direction
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
                r += dr*direction
                c += dc*direction
                if count == 4:
                    return True
    return count >= 4

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    global current_checker
    board = create_board()
    current_checker = random.choice(CHECKERS)
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        if col is None:
            print(f"Player {current_checker} loses turn due to invalid move.")
            # Switch player but don't place checker
            current_checker = CHECKERS[(CHECKERS.index(current_checker) + 1) % NUM_PLAYERS]
            continue
        
        row = place_checker(board, col, current_checker)
        print_board(board)
        
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch players
        current_checker = CHECKERS[(CHECKERS.index(current_checker) + 1) % NUM_PLAYERS]

if __name__ == '__main__':
    play_game()
