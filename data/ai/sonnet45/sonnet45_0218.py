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
    """
    Creates and returns an empty board with dimensions ROWS x COLS.
    All cells are initialized with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print horizontal border
        print("+" + "---+" * COLS)
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+" + "---+" * COLS)


def is_valid_column(board, col):
    """
    Checks if a column index is valid and has space available.
    Returns True if valid and has space, False otherwise.
    """
    if col < 0 or col >= COLS:
        return False
    # Check if top row of the column is empty
    return board[0][col] == ' '


def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from bottom row and find first empty cell
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """
    Checks if the last move at (row, col) resulted in a win.
    Checks horizontal, vertical, and both diagonal directions.
    """
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
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    count = 0
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
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    count = 0
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


def is_board_full(board):
    """
    Checks if the board is completely full (draw condition).
    """
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def get_player_move(board, player_checker):
    """
    Gets a valid column input from the player.
    Validates input and ensures column has space.
    """
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(move) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please choose between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column has space
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """
    Main game loop that handles the Connect 4 game.
    """
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
        player_checker = CHECKERS[current_player]
        
        # Get player's move
        col = get_player_move(board, player_checker)
        
        # Drop the checker
        row = drop_checker(board, col, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
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
