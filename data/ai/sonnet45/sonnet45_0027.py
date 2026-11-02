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
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print(' ', end=' ')
    for col in range(COLS):
        print(f' {chr(65 + col)} ', end=' ')
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print('+' + '---+' * COLS)
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    print('+' + '---+' * COLS)


def is_valid_column(column_input, board):
    """Check if the column input is valid and has space."""
    # Check if input is a single character
    if len(column_input) != 1:
        return False
    
    # Check if input is a letter
    if not column_input.isalpha():
        return False
    
    # Convert to column index
    col_index = ord(column_input) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space (top row must be empty)
    if board[0][col_index] != ' ':
        return False
    
    return True


def place_checker(board, column_input, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    col_index = ord(column_input) - 65
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def get_player_move(board, player_checker):
    """Get a valid move from the player."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ").upper()
        
        if is_valid_column(column_input, board):
            return column_input
        else:
            print("Invalid input. Please enter a valid column letter.")


def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get player move
        column_input = get_player_move(board, player_checker)
        
        # Place the checker
        row = place_checker(board, column_input, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, ord(column_input) - 65, player_checker):
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
