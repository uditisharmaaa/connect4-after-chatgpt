import os
import random

# Constants for board dimensions and players
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


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


def print_board(board):
    """
    Print the game board with column labels and borders.
    
    Args:
        board: The game board to print
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def get_player_input(cols):
    """
    Get and validate player input for column selection.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Validate input is within board range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: Column index (0-based)
        checker: The checker symbol to place
    
    Returns:
        True if placement was successful, False if column is full
    """
    rows = len(board)
    
    # Find the lowest empty space in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The game board
        row: Starting row
        col: Starting column
        checker: The checker symbol to check
        row_delta: Row direction (-1, 0, or 1)
        col_delta: Column direction (-1, 0, or 1)
    
    Returns:
        True if 4 checkers in a row are found, False otherwise
    """
    count = 1
    rows = len(board)
    cols = len(board[0])
    
    # Check forward direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check backward direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The game board
        row: Row of the last placed checker
        col: Column of the last placed checker
        checker: The checker symbol that was placed
    
    Returns:
        True if the player won, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, checker, 1, -1):
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_connect_four():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        print(f"Player {current_checker}, please enter a column:")
        col = get_player_input(COLUMNS)
        
        # Try to place the checker
        last_row = None
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == " ":
                last_row = row
                break
        
        if last_row is None:
            # Column is full, player loses turn
            print("Column is full. Turn skipped.")
        else:
            # Place the checker
            place_checker(board, col, current_checker)
            
            # Clear screen and print updated board
            os.system('clear')
            print_board(board)
            
            # Check for win
            if check_win(board, last_row, col, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
                break
            
            # Check for draw
            if is_board_full(board):
                print("It's a draw!")
                game_over = True
                break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_index]


if __name__ == "__main__":
    play_connect_four()
