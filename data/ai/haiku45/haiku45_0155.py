import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
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
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the board in a formatted manner.
    
    Args:
        board: The 2D list representing the board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print border between rows
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def get_valid_column(cols):
    """
    Get a valid column input from the player.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) selected by the player
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker, rows, cols):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the board
        col: The column index (0-based)
        checker: The checker symbol to place
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the checker was placed successfully, False otherwise
    """
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, row, col, checker, rows, cols):
    """
    Check if the latest placed checker results in a win.
    
    Args:
        board: The 2D list representing the board
        row: The row index of the latest placed checker
        col: The column index of the latest placed checker
        checker: The checker symbol to check
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if there are 4 in a row, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1, rows, cols):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0, rows, cols):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1, rows, cols):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, checker, 1, -1, rows, cols):
        return True
    
    return False


def check_direction(board, row, col, checker, row_delta, col_delta, rows, cols):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The 2D list representing the board
        row: The row index of the checker to start from
        col: The column index of the checker to start from
        checker: The checker symbol to check
        row_delta: The row direction (-1, 0, or 1)
        col_delta: The column direction (-1, 0, or 1)
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if there are 4 checkers in a row in the specified direction
    """
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def is_board_full(board, rows, cols):
    """
    Check if the board is completely full.
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def find_placed_row(board, col, rows):
    """
    Find the row where the last checker was placed in a column.
    
    Args:
        board: The 2D list representing the board
        col: The column index
        rows: Number of rows in the board
    
    Returns:
        The row index where the checker was placed
    """
    for row in range(rows):
        if board[row][col] != " ":
            return row
    return rows - 1


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        
        # Get valid column input
        col = get_valid_column(COLS)
        
        # Try to place the checker
        if place_checker(board, col, checker, ROWS, COLS):
            # Print the updated board
            print_board(board, COLS)
            
            # Find the row where the checker was placed
            placed_row = find_placed_row(board, col, ROWS)
            
            # Check for win
            if check_win(board, placed_row, col, checker, ROWS, COLS):
                print(f"Player {checker} won!")
                game_over = True
            # Check for draw
            elif is_board_full(board, ROWS, COLS):
                print("It's a draw!")
                game_over = True
            else:
                # Move to the next player
                current_player = (current_player + 1) % NUM_PLAYERS
        else:
            # Invalid move (column full), ask again without changing player
            print_board(board, COLS)


if __name__ == "__main__":
    play_game()
