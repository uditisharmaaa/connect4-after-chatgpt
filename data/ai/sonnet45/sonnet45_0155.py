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
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print(' ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print horizontal separator
    print('+' + '---+' * COLS)
    
    # Print each row
    for row in range(ROWS):
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
        print('+' + '---+' * COLS)


def is_valid_column(col_letter):
    """Check if the column letter is valid."""
    if len(col_letter) != 1:
        return False
    col_index = ord(col_letter) - 65
    return 0 <= col_index < COLS


def is_column_full(board, col_index):
    """Check if a column is completely full."""
    return board[0][col_index] != ' '


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    # Check if column is full
    if is_column_full(board, col_index):
        return False
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    Returns True if there are 4 in a row (horizontal, vertical, or diagonal).
    """
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
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))


def get_player_move(board, player_checker):
    """
    Get and validate player input for column selection.
    Returns the column index.
    """
    while True:
        print(f"Player {player_checker}, please enter a column: ", end='')
        col_input = input().strip().upper()
        
        # Validate input
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(col_input) - 65
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
            return None
        
        return col_index


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get player move
        col_index = get_player_move(board, current_checker)
        
        # If column was full, skip to next player
        if col_index is None:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            game_over = True
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
