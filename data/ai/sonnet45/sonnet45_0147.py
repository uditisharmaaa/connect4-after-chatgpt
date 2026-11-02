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
    """Print the game board with column labels."""
    # Clear screen
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print rows with checkers
    for row in range(ROWS):
        print('  +' + '---+' * COLS)
        print('  |', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    # Print bottom border
    print('  +' + '---+' * COLS)


def is_valid_column(column_input):
    """Check if the column input is a valid letter."""
    if len(column_input) != 1:
        return False
    return column_input.isalpha() and column_input.isupper()


def column_letter_to_index(column_letter):
    """Convert column letter to column index."""
    return ord(column_letter) - 65


def is_column_in_range(col_index):
    """Check if column index is within board range."""
    return 0 <= col_index < COLS


def is_column_full(board, col_index):
    """Check if a column is completely filled."""
    return board[0][col_index] != ' '


def place_checker(board, col_index, checker):
    """Place a checker in the specified column. Returns True if successful."""
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the specified checker has won the game."""
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
    """Check if the board is completely full."""
    return all(board[0][col] != ' ' for col in range(COLS))


def get_player_move(board, player_checker):
    """Get and validate player move input."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Validate input is a single uppercase letter
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        
        col_index = column_letter_to_index(column_input)
        
        # Check if column is within board range
        if not is_column_in_range(col_index):
            print(f"Column out of range. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        
        # Get valid move from player
        col_index = get_player_move(board, current_checker)
        
        # Place checker
        place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("Game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
