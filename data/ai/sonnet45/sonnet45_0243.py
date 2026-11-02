import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and grid lines."""
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print rows with grid lines
    for row in range(ROWS):
        # Print top border of cells
        print('  +', end='')
        for col in range(COLS):
            print('---+', end='')
        print()
        
        # Print cell content
        print('  |', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    # Print bottom border
    print('  +', end='')
    for col in range(COLS):
        print('---+', end='')
    print()


def is_valid_column(col_letter, board):
    """Check if the column input is valid and has space."""
    # Check if input is a single uppercase letter
    if len(col_letter) != 1 or not col_letter.isupper() or not col_letter.isalpha():
        return False, "Invalid input. Please enter a single uppercase letter."
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False, "Column out of bounds. Please choose a valid column."
    
    # Check if column has space (top row must be empty)
    if board[0][col_index] != ' ':
        return False, "Column is full. Please choose another column."
    
    return True, col_index


def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available row."""
    # Start from the bottom row and find the first empty cell
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, checker, -1, 1):
        return True
    
    return False


def check_direction(board, row, col, checker, row_delta, col_delta):
    """Check for WIN_LENGTH consecutive checkers in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    count += count_consecutive(board, row, col, checker, row_delta, col_delta)
    
    # Check in negative direction
    count += count_consecutive(board, row, col, checker, -row_delta, -col_delta)
    
    return count >= WIN_LENGTH


def count_consecutive(board, row, col, checker, row_delta, col_delta):
    """Count consecutive checkers in a given direction."""
    count = 0
    current_row = row + row_delta
    current_col = col + col_delta
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == checker):
        count += 1
        current_row += row_delta
        current_col += col_delta
    
    return count


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def get_player_move(board, player_checker):
    """Get and validate player move input."""
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ")
        valid, result = is_valid_column(col_input, board)
        
        if valid:
            return result
        else:
            print(result)


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        player_checker = CHECKERS[current_player]
        
        # Get player move
        col_index = get_player_move(board, player_checker)
        
        # Place checker
        row_placed = place_checker(board, col_index, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_placed, col_index, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
