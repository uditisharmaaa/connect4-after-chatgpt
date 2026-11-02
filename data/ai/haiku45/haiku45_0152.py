import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board(rows, cols):
    """
    Creates and returns an empty board of given dimensions.
    Each cell is initialized with a space character.
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Prints the current state of the board with proper formatting.
    Includes column labels (A, B, C, ...) and border characters.
    """
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print rows with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def get_column_input(num_players, current_player):
    """
    Gets and validates column input from the current player.
    Returns the column index (0-6) or -1 if invalid.
    """
    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, current_player):
    """
    Places a checker in the specified column.
    Returns True if placement was successful, False if column is full.
    """
    checker = CHECKERS[current_player]
    
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, row, col, player):
    """
    Checks if the current player has won by placing a checker at (row, col).
    Returns True if the player has 4 in a row, False otherwise.
    """
    checker = CHECKERS[player]
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < cols and board[row][c] == checker:
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
    while r < rows and board[r][col] == checker:
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
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if the board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def get_placement_row(board, col):
    """
    Returns the row index where a checker would be placed in the given column.
    Returns -1 if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1


def play_game():
    """
    Main game loop. Handles player turns, input validation, win checking, etc.
    """
    board = create_board(ROWS, COLS)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        # Get valid column input
        while True:
            col = get_column_input(NUM_PLAYERS, current_player)
            
            # Try to place checker
            placement_row = get_placement_row(board, col)
            if placement_row == -1:
                print("This column is full. Please choose another column.")
                continue
            
            # Place checker successfully
            place_checker(board, col, current_player)
            break
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, placement_row, col, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
