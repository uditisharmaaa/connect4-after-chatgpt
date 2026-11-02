import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
current_player = 0

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(COLS)]
    print('  ' + '   '.join(headers))
    
    # Print each row with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    
    print(border)

def validate_column_input(col_input):
    """Validate the player's column input."""
    if len(col_input) != 1:
        return False
    col_char = col_input.upper()
    if not col_char.isalpha():
        return False
    col_num = ord(col_char) - ord('A')
    return 0 <= col_num < COLS

def place_checker(board, player_checker, col_char):
    """Place the player's checker in the specified column.
    Returns True if placement was successful."""
    col_num = ord(col_char.upper()) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_num] == ' ':
            board[row][col_num] = player_checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the specified checker has won."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def board_is_full(board):
    """Check if the board is full."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    global current_player
    board = initialize_board()
    player_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        checker = player_checkers[current_player]
        print_board(board)
        
        # Get player input
        while True:
            col_input = input(f"Player {checker}, please enter a column: ").strip()
            if validate_column_input(col_input):
                col_char = col_input.upper()
                if place_checker(board, checker, col_char):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
        
        # Check for win
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if board_is_full(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
