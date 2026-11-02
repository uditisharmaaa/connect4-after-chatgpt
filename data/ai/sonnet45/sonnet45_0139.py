import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
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


def is_valid_column(col_letter, board):
    """Check if the column letter is valid and not full."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - ord('A')
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True


def place_checker(board, col_letter, checker):
    """Place a checker in the specified column."""
    col_index = ord(col_letter) - ord('A')
    
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
    
    # Check diagonal (top-left to bottom-right)
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
    
    # Check diagonal (bottom-left to top-right)
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


def check_draw(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def get_player_input(player_checker, board):
    """Get and validate player input."""
    while True:
        col_letter = input(f"Player {player_checker}, please enter a column: ").upper()
        
        if is_valid_column(col_letter, board):
            return col_letter
        else:
            print("Invalid input. Please enter a valid column letter that is not full.")


def play_game():
    """Main game loop."""
    board = create_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        
        # Get player input
        col_letter = get_player_input(checker, board)
        
        # Place checker
        row, col = place_checker(board, col_letter, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
