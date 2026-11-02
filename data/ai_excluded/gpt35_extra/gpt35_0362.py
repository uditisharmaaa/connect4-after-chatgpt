import os
import random

# Constants for the game configuration
ROWS = 6            # Number of rows (height)
COLUMNS = 7         # Number of columns (width), max 26
NUM_PLAYERS = 2     # Number of players (2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players in order

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a rows x cols board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board with column labels (A-G),
    rows have no labels.
    """
    clear_screen()
    # Print column headers, letters from 'A' with length = columns
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    
    # Print board rows separated by horizontal lines
    for row in board:
        print('+' + '---+' * len(row))      # horizontal separator
        # Each cell in this row enclosed by |
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * len(board[0]))

def is_valid_input(user_input, columns):
    """
    Validates if the user input is a single uppercase letter corresponding to a column
    """
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col_index = ord(user_input) - ord('A')
    if col_index < 0 or col_index >= columns:
        return False
    return True

def get_column_index(user_input):
    """Converts column letter to zero-based index."""
    return ord(user_input) - ord('A')

def place_checker(board, col, checker):
    """
    Tries to place a checker in the specified column.
    The checker falls to the lowest available space.
    Returns True if placed successfully, False if column is full.
    """
    # Start from bottom row and go upwards
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    """
    Checks if the given checker has 4 in a row horizontally,
    vertically or diagonally anywhere on the board.
    Returns True if win is found.
    """
    rows = len(board)
    cols = len(board[0])
    required = 4
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - required + 1):
            if all(board[r][c + offset] == checker for offset in range(required)):
                return True
    
    # Check vertical
    for c in range(cols):
        for r in range(rows - required + 1):
            if all(board[r + offset][c] == checker for offset in range(required)):
                return True

    # Check diagonal down-right
    for r in range(rows - required + 1):
        for c in range(cols - required + 1):
            if all(board[r + offset][c + offset] == checker for offset in range(required)):
                return True
    
    # Check diagonal up-right
    for r in range(required - 1, rows):
        for c in range(cols - required + 1):
            if all(board[r - offset][c + offset] == checker for offset in range(required)):
                return True
    
    return False

def check_draw(board):
    """
    Checks if the board is full (no spaces left).
    Returns True if draw.
    """
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Limit players and board size according to assignment constants
    assert ROWS == 6 and COLUMNS == 7 and NUM_PLAYERS == 2, \
        "For submission, set ROWS=6, COLUMNS=7 and NUM_PLAYERS=2"

    board = create_board(ROWS, COLUMNS)
    
    # Choose first player randomly - index in players list
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        checker = CHECKERS[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        
        # Get valid input
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_input(user_input, COLUMNS):
                print(f"Invalid input '{user_input}'. Please enter a valid column letter A-{chr(ord('A')+COLUMNS-1)}.")
                continue
            col = get_column_index(user_input)
            # Check if column is full -> turn lost if full
            if board[0][col] != ' ':
                # Column full, turn lost
                print(f"Column {user_input} is full. Turn lost.")
                break  # skip turn by breaking inner input loop
            # Valid input and column not full
            # Place checker
            placed = place_checker(board, col, checker)
            if not placed:
                # Shouldn't happen because we checked top row, but safe check
                print(f"Column {user_input} is full. Turn lost.")
            break
        
        # If we didn't place a checker, move to next player (turn lost)
        if board[0][col] != checker:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check win condition for current player
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        # Check draw condition
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
