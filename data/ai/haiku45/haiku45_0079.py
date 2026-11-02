import os
import random

# Constants for board configuration
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board filled with spaces
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def get_column_label(col_index):
    """
    Convert column index to letter label.
    
    Args:
        col_index: Index of the column (0-based)
    
    Returns:
        The letter corresponding to the column
    """
    return chr(ord('A') + col_index)


def print_board(board, cols, rows):
    """
    Print the current state of the board.
    
    Args:
        board: The current board state
        cols: Number of columns
        rows: Number of rows
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{get_column_label(col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def is_valid_move(board, col, cols, rows):
    """
    Check if a move is valid (column exists and is not full).
    
    Args:
        board: The current board state
        col: Column index (0-based)
        cols: Total number of columns
        rows: Total number of rows
    
    Returns:
        True if the move is valid, False otherwise
    """
    if col < 0 or col >= cols:
        return False
    
    # Check if the top cell of the column is empty
    if board[0][col] != ' ':
        return False
    
    return True


def get_player_input(cols):
    """
    Get and validate player input for column selection.
    
    Args:
        cols: Total number of columns
    
    Returns:
        Column index (0-based) that the player selected
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {get_column_label(cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker, rows):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The current board state
        col: Column index (0-based)
        checker: The checker symbol (character)
        rows: Total number of rows
    
    Returns:
        The row index where the checker was placed
    """
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    
    return -1  # Column is full


def check_win(board, col, row, checker, cols, rows):
    """
    Check if the last move resulted in a win.
    
    Args:
        board: The current board state
        col: Column index of the last move (0-based)
        row: Row index of the last move (0-based)
        checker: The checker symbol that was placed
        cols: Total number of columns
        rows: Total number of rows
    
    Returns:
        True if the move resulted in a win, False otherwise
    """
    # Check horizontal
    if check_direction(board, col, row, checker, 0, 1, cols, rows):
        return True
    
    # Check vertical
    if check_direction(board, col, row, checker, 1, 0, cols, rows):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, col, row, checker, 1, 1, cols, rows):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, col, row, checker, 1, -1, cols, rows):
        return True
    
    return False


def check_direction(board, col, row, checker, row_delta, col_delta, cols, rows):
    """
    Check if there are WIN_LENGTH checkers in a row in a specific direction.
    
    Args:
        board: The current board state
        col: Column index of the reference point (0-based)
        row: Row index of the reference point (0-based)
        checker: The checker symbol to search for
        row_delta: Row direction (-1, 0, or 1)
        col_delta: Column direction (-1, 0, or 1)
        cols: Total number of columns
        rows: Total number of rows
    
    Returns:
        True if WIN_LENGTH checkers are found in the direction, False otherwise
    """
    count = 1  # Count the checker at (row, col)
    
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


def is_board_full(board, cols, rows):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The current board state
        cols: Total number of columns
        rows: Total number of rows
    
    Returns:
        True if the board is full, False otherwise
    """
    for col in range(cols):
        if board[0][col] == ' ':
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
    
    # Display initial board
    print_board(board, COLS, ROWS)
    
    # Main game loop
    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Prompt for input and validate
        print(f"Player {checker}, please enter a column:", end=" ")
        col = get_player_input(COLS)
        
        # Check if the move is valid
        if not is_valid_move(board, col, COLS, ROWS):
            print("Column is full. Please try another column.")
            continue
        
        # Place the checker
        row = place_checker(board, col, checker, ROWS)
        
        # Print updated board
        print_board(board, COLS, ROWS)
        
        # Check for win
        if check_win(board, col, row, checker, COLS, ROWS):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, COLS, ROWS):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
