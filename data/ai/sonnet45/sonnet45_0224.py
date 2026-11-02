import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print board rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Check if column is within board range
    col_index = ord(col_letter) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, checker):
    """Place a checker in the specified column."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    
    return -1, -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_COUNT:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_COUNT:
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
            if count >= WIN_COUNT:
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
            if count >= WIN_COUNT:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        col_input = input().strip()
        
        # Validate input
        while not is_valid_column(col_input, board):
            print_board(board)
            print(f"Invalid input. Player {checker}, please enter a valid column: ", end="")
            col_input = input().strip()
        
        # Place checker
        row, col = place_checker(board, col_input, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
