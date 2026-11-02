import os
import random

# Global constants for board configuration
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the game board with column labels and formatting.
    
    Args:
        board: The game board to print
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in board:
        # Print top border
        print("+---" * cols + "+")
        # Print row content
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def get_column_input(cols, board):
    """
    Get and validate column input from the player.
    
    Args:
        cols: Number of columns in the board
        board: The game board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input().strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(65 + cols - 1)))
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-{}).".format(chr(65 + cols - 1)))
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Validate column is within bounds
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Please enter a letter between A and {}.".format(chr(65 + cols - 1)))
            continue
        
        # Validate column is not full
        if board[0][col_index] != " ":
            print("Column {} is full. Please choose another column.".format(user_input))
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col_index: The column index where to place the checker
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if column is full
    """
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker, rows, cols):
    """
    Check if the player has won after placing a checker.
    
    Args:
        board: The game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker symbol to check for
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the player has won, False otherwise
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
    # Check top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check bottom-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check bottom-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board, cols):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board
        cols: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for col in range(cols):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    print(f"Player {CHECKERS[current_player]}, please enter a column:")
    
    # Game loop
    while True:
        # Get column input from current player
        col_index = get_column_input(COLUMNS, board)
        
        # Place checker
        row_index = place_checker(board, col_index, CHECKERS[current_player])
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, row_index, col_index, CHECKERS[current_player], ROWS, COLUMNS):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if is_board_full(board, COLUMNS):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS
        
        # Prompt next player
        print(f"Player {CHECKERS[current_player]}, please enter a column:")


if __name__ == "__main__":
    play_game()
