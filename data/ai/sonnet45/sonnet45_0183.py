import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and return an empty board with given dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print separator
    print('  ', end='')
    for col in range(COLS):
        print('+---', end='')
    print('+')
    
    # Print rows
    for row in range(ROWS):
        print('  ', end='')
        for col in range(COLS):
            print(f'| {board[row][col]} ', end='')
        print('|')
        
        # Print separator
        print('  ', end='')
        for col in range(COLS):
            print('+---', end='')
        print('+')


def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != ' ':
        return False
    
    return True


def place_checker(board, col_letter, checker):
    """Place a checker in the specified column."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index
    
    return None, None


def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, checker, -1, 1):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    return False


def check_direction(board, row, col, checker, delta_row, delta_col):
    """Check if there are 4 checkers in a row in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + delta_row, col + delta_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    
    # Check in negative direction
    r, c = row - delta_row, col - delta_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col
    
    return count >= WIN_LENGTH


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        col_input = input().strip()
        
        # Validate input
        if not is_valid_column(col_input, board):
            print_board(board)
            print("Invalid input! Please enter a valid column letter.")
            continue
        
        # Place checker
        row, col = place_checker(board, col_input, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
