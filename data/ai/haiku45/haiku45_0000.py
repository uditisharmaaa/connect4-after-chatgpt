import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board in the required format.
    
    Args:
        board: The 2D list representing the board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * cols + "+")


def is_valid_column(col_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        col_input: The user input for the column
        cols: Number of columns in the board
    
    Returns:
        The column index if valid, -1 otherwise
    """
    if len(col_input) != 1:
        return -1
    
    if not col_input.isalpha():
        return -1
    
    col_input = col_input.upper()
    col_index = ord(col_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def can_place_checker(board, col):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The 2D list representing the board
        col: The column index
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][col] == " "


def place_checker(board, col, checker):
    """
    Place a checker in the given column.
    
    Args:
        board: The 2D list representing the board
        col: The column index
        checker: The checker symbol
    
    Returns:
        The row where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The 2D list representing the board
        row: The row where the checker was placed
        col: The column where the checker was placed
        checker: The checker symbol
    
    Returns:
        True if there's a win, False otherwise
    """
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


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The 2D list representing the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get player input
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {checker}, please enter a column: ")
            col = is_valid_column(col_input, COLS)
            
            if col == -1:
                print("Invalid input. Please enter a valid column (A-" + chr(ord('A') + COLS - 1) + ").")
                continue
            
            if not can_place_checker(board, col):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row = place_checker(board, col, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
