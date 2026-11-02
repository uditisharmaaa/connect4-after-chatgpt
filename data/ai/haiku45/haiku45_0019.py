import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the current state of the board in a formatted manner.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with separators
    for row in range(rows):
        # Print top separator
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom separator
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()


def get_valid_column_input(board):
    """
    Get a valid column input from the player.
    
    Args:
        board: The game board
    
    Returns:
        The column index (0-based) where the checker should be placed
    """
    cols = len(board[0])
    
    while True:
        user_input = input("Please enter a column (A-{}): ".format(chr(65 + cols - 1))).strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print("Invalid column. Please enter a letter between A and {}.".format(chr(65 + cols - 1)))
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col_index: The column index (0-based) where the checker should be placed
        checker: The checker symbol to place
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
        count += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # Check down
    i = row + 1
    while i < rows and board[i][col] == checker:
        count += 1
        i += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # Check down-right
    i, j = row + 1, col + 1
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def get_last_checker_position(board, col_index):
    """
    Get the row index of the last placed checker in a column.
    
    Args:
        board: The game board
        col_index: The column index (0-based)
    
    Returns:
        The row index of the last placed checker, or -1 if column is empty
    """
    rows = len(board)
    
    for row in range(rows):
        if board[row][col_index] != " ":
            return row
    
    return -1


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Starting player: {CHECKERS[current_player_index]}")
    input("Press Enter to begin...")
    
    game_over = False
    
    while not game_over:
        print_board(board)
        
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column input
        col_index = get_valid_column_input(board)
        
        # Place the checker
        place_checker(board, col_index, current_checker)
        
        # Get the row where the checker was placed
        last_row = get_last_checker_position(board, col_index)
        
        # Check for win
        if check_win(board, last_row, col_index, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
