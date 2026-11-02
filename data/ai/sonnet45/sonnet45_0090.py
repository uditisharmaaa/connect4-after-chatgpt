import random
import os

# Global constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and return an empty board with specified dimensions."""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board


def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print top border
        print("+" + "---+" * COLS)
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+" + "---+" * COLS)


def is_valid_column(col_letter, board):
    """Check if the column input is valid and has space."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - ord('A')
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space (top row is not full)
    if board[0][col_index] != ' ':
        return False
    
    return True


def place_checker(board, col_letter, checker):
    """Place a checker in the specified column at the lowest available position."""
    col_index = ord(col_letter) - ord('A')
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index
    
    return -1, -1  # Should not happen if validation is correct


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
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    # Count along diagonal
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
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    # Count along diagonal
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
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Prompt player for input
        col_input = input(f"Player {checker}, please enter a column: ")
        
        # Validate input
        while not is_valid_column(col_input, board):
            print("Invalid input. Please enter a valid column letter.")
            col_input = input(f"Player {checker}, please enter a column: ")
        
        # Place the checker
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
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


# Start the game
if __name__ == "__main__":
    play_game()
