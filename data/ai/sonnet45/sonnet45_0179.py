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
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print board rows
    for row in range(ROWS):
        # Print top border
        print('  +', end='')
        for col in range(COLS):
            print('---+', end='')
        print()
        
        # Print row content
        print('  |', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    # Print bottom border
    print('  +', end='')
    for col in range(COLS):
        print('---+', end='')
    print()


def is_valid_column(column_input):
    """Check if the column input is a valid uppercase letter."""
    if len(column_input) != 1:
        return False
    if not column_input.isupper():
        return False
    if not column_input.isalpha():
        return False
    return True


def get_column_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter) - ord('A')


def is_column_in_range(col_index):
    """Check if column index is within board range."""
    return 0 <= col_index < COLS


def get_lowest_available_row(board, col):
    """Find the lowest available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1


def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    row = get_lowest_available_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True


def check_win(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely filled."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True


def get_player_move(board, player_checker):
    """Get and validate player move."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Validate input format
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid uppercase letter.")
            continue
        
        # Convert to column index
        col_index = get_column_index(column_input)
        
        # Check if column is in range
        if not is_column_in_range(col_index):
            print("Column out of range. Please try again.")
            continue
        
        # Check if column is full
        if get_lowest_available_row(board, col_index) == -1:
            print("Column is full. You lose your turn.")
            return -1
        
        return col_index


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Initialize players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = players[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_checker)
        
        # Place checker (if valid move)
        if col != -1:
            place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if col != -1 and check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
