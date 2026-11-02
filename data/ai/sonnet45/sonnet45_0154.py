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
    Each cell is initialized with a space character.
    """
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print top border of row
        print("+---" * COLS + "+")
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def get_valid_column(board, player_checker):
    """
    Prompts the player for a column input and validates it.
    Returns the column index (0-based) when valid input is received.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase and check if it's a letter
        user_input = user_input.upper()
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within board bounds
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLS)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != ' ':
            print("Column is full. You lose your turn.")
            return -1  # Return -1 to indicate full column (turn lost)
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Places the checker in the specified column at the lowest available row.
    Returns the row index where the checker was placed, or -1 if column is full.
    """
    # Start from bottom row and move up to find empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """
    Checks if the last move at (row, col) resulted in a win.
    Checks horizontal, vertical, and both diagonal directions.
    Returns True if there are 4 in a row, False otherwise.
    """
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Checks if the board is completely full (draw condition).
    Returns True if board is full, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def play_game():
    """
    Main game loop that handles the Connect 4 game.
    """
    # Initialize the game
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid column from player
        col_index = get_valid_column(board, current_checker)
        
        # If column was full, skip to next player
        if col_index == -1:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        # Place the checker
        row_index = place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Start the game
if __name__ == "__main__":
    play_game()
