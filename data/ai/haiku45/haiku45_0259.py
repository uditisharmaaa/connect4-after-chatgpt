import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
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
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the game board with column labels and formatting.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(cols):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_column(column, cols):
    """
    Validate if the column input is valid.
    
    Args:
        column: The column input (string)
        cols: Number of columns
    
    Returns:
        True if valid column letter, False otherwise
    """
    if len(column) != 1:
        return False
    if not column.isalpha():
        return False
    if not column.isupper():
        return False
    
    col_index = ord(column) - ord('A')
    return 0 <= col_index < cols


def get_column_from_input(column_letter, cols):
    """
    Convert column letter to column index.
    
    Args:
        column_letter: The column letter (string)
        cols: Number of columns
    
    Returns:
        Column index (0-based)
    """
    return ord(column_letter) - ord('A')


def can_place_checker(board, col_index, rows):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The game board (2D list)
        col_index: The column index
        rows: Number of rows
    
    Returns:
        True if the column is not full, False otherwise
    """
    return board[0][col_index] == " "


def place_checker(board, col_index, checker, rows):
    """
    Place a checker in the given column and return the row where it was placed.
    
    Args:
        board: The game board (2D list)
        col_index: The column index
        checker: The checker symbol
        rows: Number of rows
    
    Returns:
        The row index where the checker was placed
    """
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_direction(board, row, col, checker, d_row, d_col, rows, cols):
    """
    Check if there are 4 consecutive checkers in a given direction.
    
    Args:
        board: The game board (2D list)
        row: Starting row
        col: Starting column
        checker: The checker symbol to check
        d_row: Direction row offset (-1, 0, or 1)
        d_col: Direction column offset (-1, 0, or 1)
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if 4 consecutive checkers found, False otherwise
    """
    count = 1
    
    # Check in positive direction
    r, c = row + d_row, col + d_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col
    
    # Check in negative direction
    r, c = row - d_row, col - d_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= d_row
        c -= d_col
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker, rows, cols):
    """
    Check if the last placed checker results in a win.
    
    Args:
        board: The game board (2D list)
        row: Row of the last placed checker
        col: Column of the last placed checker
        checker: The checker symbol
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if the player won, False otherwise
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


def is_board_full(board, rows, cols):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    board = initialize_board(ROWS, COLS)
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    while True:
        # Get player input
        while True:
            column_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            if not is_valid_column(column_input, COLS):
                print("Invalid input. Please enter a valid column letter (A-{}).".format(
                    chr(ord('A') + COLS - 1)))
                continue
            
            col_index = get_column_from_input(column_input, COLS)
            
            if not can_place_checker(board, col_index, ROWS):
                print("This column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker
        row = place_checker(board, col_index, current_checker, ROWS)
        
        # Print the updated board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, row, col_index, current_checker, ROWS, COLS):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_index]


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
