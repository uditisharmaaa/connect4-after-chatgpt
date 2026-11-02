import os
import random

# Configuration constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def init_board():
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)} ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def is_column_valid(col_letter):
    """Check if column letter is valid."""
    if len(col_letter) != 1 or not col_letter.isalpha():
        return False
    col = ord(col_letter.upper()) - ord('A')
    return 0 <= col < COLS

def get_column_index(col_letter):
    """Convert column letter to index."""
    return ord(col_letter.upper()) - ord('A')

def can_place_checker(board, col):
    """Check if a checker can be placed in the column."""
    return board[0][col] == " "

def place_checker(board, col, checker):
    """Place a checker in the column and return the row where it was placed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last placed checker resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    board = init_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checker = CHECKERS[current_player]
    
    print_board(board)
    
    while True:
        # Get player input
        while True:
            col_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            
            if not is_column_valid(col_input):
                print("Invalid input. Please enter a valid column (A-{}).".format(chr(65 + COLS - 1)))
                continue
            
            col = get_column_index(col_input)
            
            if not can_place_checker(board, col):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place checker
        row = place_checker(board, col, checker)
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % NUM_PLAYERS
        checker = CHECKERS[current_player]

if __name__ == "__main__":
    play_game()
