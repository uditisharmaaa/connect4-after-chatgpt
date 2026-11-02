import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def create_board():
    """Create and return an empty board with specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_column(board, col_letter):
    """Check if the column input is valid and has space."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is a letter
    if not col_letter.isalpha():
        return False
    
    # Convert to column index
    col_index = ord(col_letter.upper()) - ord('A')
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space (top row is empty)
    if board[0][col_index] != " ":
        return False
    
    return True

def get_column_input(board, player_checker):
    """Get valid column input from player."""
    while True:
        col_letter = input(f"Player {player_checker}, please enter a column: ")
        
        if is_valid_column(board, col_letter):
            return ord(col_letter.upper()) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter with available space.")

def place_checker(board, col, checker):
    """Place the checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_horizontal(board, row, col, checker):
    """Check for horizontal win starting from position (row, col)."""
    count = 0
    # Check all positions in the row
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_vertical(board, row, col, checker):
    """Check for vertical win starting from position (row, col)."""
    count = 0
    # Check all positions in the column
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_diagonal(board, row, col, checker):
    """Check for diagonal wins (both directions) involving position (row, col)."""
    # Check diagonal (top-left to bottom-right)
    for start_row in range(ROWS):
        for start_col in range(COLS):
            count = 0
            r, c = start_row, start_col
            while r < ROWS and c < COLS:
                if board[r][c] == checker:
                    count += 1
                    if count >= WIN_LENGTH:
                        return True
                else:
                    count = 0
                r += 1
                c += 1
    
    # Check anti-diagonal (top-right to bottom-left)
    for start_row in range(ROWS):
        for start_col in range(COLS):
            count = 0
            r, c = start_row, start_col
            while r < ROWS and c >= 0:
                if board[r][c] == checker:
                    count += 1
                    if count >= WIN_LENGTH:
                        return True
                else:
                    count = 0
                r += 1
                c -= 1
    
    return False

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    if check_horizontal(board, row, col, checker):
        return True
    if check_vertical(board, row, col, checker):
        return True
    if check_diagonal(board, row, col, checker):
        return True
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid column input
        col = get_column_input(board, checker)
        
        # Place checker
        row = place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
