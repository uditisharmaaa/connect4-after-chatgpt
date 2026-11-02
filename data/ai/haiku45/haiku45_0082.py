import os
import random

# Constants for game configuration
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the game board with proper formatting.
    
    Args:
        board: The current game board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * cols + "+")


def column_letter_to_index(letter, cols):
    """
    Convert a column letter (A, B, C, etc.) to its index.
    
    Args:
        letter: The column letter input by the player
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) or -1 if invalid
    """
    if len(letter) != 1 or not letter.isalpha():
        return -1
    
    letter = letter.upper()
    col_index = ord(letter) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def is_valid_move(board, col_index, cols):
    """
    Check if a move is valid (column exists and is not full).
    
    Args:
        board: The current game board
        col_index: The column index to check
        cols: Number of columns in the board
    
    Returns:
        True if the move is valid, False otherwise
    """
    if col_index < 0 or col_index >= cols:
        return False
    
    # Check if the top cell of the column is empty
    if board[0][col_index] == " ":
        return True
    
    return False


def get_valid_move(board, cols):
    """
    Get a valid move from the player with input validation.
    
    Args:
        board: The current game board
        cols: Number of columns in the board
    
    Returns:
        The valid column index (0-based)
    """
    while True:
        user_input = input("Please enter a column (A-" + chr(ord('A') + cols - 1) + "): ").strip()
        
        col_index = column_letter_to_index(user_input, cols)
        
        if col_index == -1:
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        if not is_valid_move(board, col_index, cols):
            print("That column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column (drops to lowest available row).
    
    Args:
        board: The current game board
        col_index: The column index where the checker will be placed
        checker: The checker symbol (X, O, V, H, M)
    
    Returns:
        The row index where the checker was placed
    """
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker, rows, cols):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The current game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the checker wins, False otherwise
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
    Check if there are WIN_LENGTH checkers in a row in a specific direction.
    
    Args:
        board: The current game board
        row: The row index of the starting checker
        col: The column index of the starting checker
        checker: The checker symbol to check for
        row_delta: The row direction (-1, 0, or 1)
        col_delta: The column direction (-1, 0, or 1)
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if WIN_LENGTH checkers in a row are found, False otherwise
    """
    count = 1  # Count the current checker
    
    # Check in the positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in the negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def is_board_full(board, rows, cols):
    """
    Check if the board is completely filled.
    
    Args:
        board: The current game board
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def main():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get the checkers for each player
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board, COLUMNS)
    print(f"Player {checkers[current_player_index]} will start first!")
    input("Press Enter to start the game...")
    
    game_over = False
    winner = None
    
    # Main game loop
    while not game_over:
        # Print the current board
        print_board(board, COLUMNS)
        
        current_checker = checkers[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        # Get a valid move from the current player
        col_index = get_valid_move(board, COLUMNS)
        
        # Place the checker
        row_index = place_checker(board, col_index, current_checker)
        
        # Check if the current player won
        if check_win(board, row_index, col_index, current_checker, ROWS, COLUMNS):
            print_board(board, COLUMNS)
            print(f"Player {current_checker} won!")
            game_over = True
            winner = current_checker
        
        # Check if the board is full (draw)
        elif is_board_full(board, ROWS, COLUMNS):
            print_board(board, COLUMNS)
            print("The board is full. It's a draw!")
            game_over = True
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
