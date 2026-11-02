import os
import random

# Constants for the board size and players
ROWS = 6
COLS = 7
MAX_COLS = 26  # max columns allowed according to assignment
WIN_COUNT = 4  # number of checkers in a row to win
PLAYERS = 2    # number of players (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # checkers for up to 5 players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create the initial game board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    cols = len(board[0])
    # Print column labels A, B, C, ...
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(labels)
    
    # Print horizontal separator line
    line_sep = "+" + "---+" * cols
    
    for row in board:
        print(line_sep)
        # Print each cell separated by |
        print("| " + " | ".join(row) + " |")
    print(line_sep)

def is_valid_column(input_col, cols):
    """Check if the input column is a valid uppercase letter in the board range."""
    if len(input_col) != 1:
        return False
    if not ('A' <= input_col <= chr(ord('A') + cols - 1)):
        return False
    return True

def column_index(col_letter):
    """Convert column letter to board index."""
    return ord(col_letter) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place a checker in the specified column if possible.
    The checker falls down to the lowest available row.
    Returns True if placed, False if the column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # column is full

def board_full(board):
    """Check if the board is completely full (no spaces left)."""
    for row in board:
        if " " in row:
            return False
    return True

def check_winner(board, checker):
    """
    Check the board if the player with 'checker' has 4 in a row horizontally,
    vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
    
    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
    
    # Diagonal (bottom-left to top-right) check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    
    # Diagonal (top-left to bottom-right) check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    
    return False

def get_valid_input(current_player, cols):
    """
    Prompt the current player to enter a valid column letter.
    Validate the input to ensure it is uppercase and within range.
    Return the column letter.
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, cols):
            # Invalid input: not single letter or out of range
            continue
        return user_input

def main():
    # Initialize the game board
    board = create_board(ROWS, COLS)
    
    # Determine the players for the game (subset of CHECKERS)
    players = CHECKERS[:PLAYERS]
    
    # Randomly select starting player index
    current_player_idx = random.randint(0, PLAYERS - 1)

    # Print initial game board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = players[current_player_idx]
        
        # Get valid input from current player
        col_letter = get_valid_input(current_checker, COLS)
        col_idx = column_index(col_letter)
        
        # Attempt to place checker
        placed = place_checker(board, col_idx, current_checker)
        if not placed:
            # Column full -> player loses turn
            # Just print the board and continue to next player
            print_board(board)
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check if board is full (draw)
        if board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
