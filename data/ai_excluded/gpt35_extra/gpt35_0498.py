import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
# Player checkers in order for up to 5 players
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates the game board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column labels and grid lines."""
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(col_labels))
    
    # Print top border line
    print('+' + '---+' * cols)
    
    # Print each row of the board
    for r in range(rows):
        row_str = '|'
        for c in range(cols):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
        print('+' + '---+' * cols)

def is_valid_column(input_str, cols):
    """Checks if the input is a valid column letter in uppercase."""
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    return 'A' <= letter < chr(ord('A') + cols)

def get_column_index(col_letter):
    """Converts column letter to zero-based column index."""
    return ord(col_letter.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Attempts to place a checker in the given column.
    Returns True if placed successfully, False if column is full.
    """
    rows = len(board)
    # Place checker on the lowest available row in the column
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return True
    return False  # Column full

def check_horizontal(board, checker):
    """Checks for horizontal 4 in a row for the given checker."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

def check_vertical(board, checker):
    """Checks for vertical 4 in a row for the given checker."""
    rows = len(board)
    cols = len(board[0])
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

def check_diagonal(board, checker):
    """
    Checks for diagonal 4 in a row (both directions)
    for the given checker.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check / diagonals (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True
                
    # Check \ diagonals (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True

    return False

def check_win(board, checker):
    """Checks if the given checker has achieved 4 in a row."""
    return (check_horizontal(board, checker) or
            check_vertical(board, checker) or
            check_diagonal(board, checker))

def board_full(board):
    """Checks if the board is full (no empty spaces)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Initialize board and players
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        
        # Prompt player input, validate input, repeat if invalid
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip()
            if not is_valid_column(user_input, COLS):
                # Invalid input: not a single uppercase letter in range
                print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
                continue
            
            col_idx = get_column_index(user_input)
            # Attempt to place the checker
            placed = place_checker(board, col_idx, current_checker)
            if not placed:
                # Column full, player loses turn as per instructions
                # Inform the player and break to next player's turn
                print(f"Column {user_input.upper()} is full. You lose your turn.")
                break
            else:
                # Valid placement, move to next phase
                break
        
        # Check win only if placement was successful
        # If placement failed, no need to check win condition
        if placed:
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            
            # Check draw condition
            if board_full(board):
                print_board(board)
                print("The game is a draw!")
                break
        
        # Proceed to next player (circular)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
