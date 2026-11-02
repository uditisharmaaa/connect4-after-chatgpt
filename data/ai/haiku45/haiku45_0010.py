import random
import os

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, columns):
    """
    Initialize the board with all empty cells (whitespaces).
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[' ' for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board in a formatted manner with column labels and borders.
    
    Args:
        board: The game board (2D list)
    """
    os.system('clear')
    rows = len(board)
    columns = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(columns):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+", end="")
        for col in range(columns):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(columns):
        print("---+", end="")
    print()


def get_valid_input(board):
    """
    Get and validate user input for column selection.
    
    Args:
        board: The game board (2D list)
    
    Returns:
        The column index (0-based) where the checker should be placed
    """
    columns = len(board[0])
    
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
        if col_index < 0 or col_index >= columns:
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + columns - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The game board (2D list)
        col_index: The column index (0-based)
        checker: The checker symbol (X, O, V, H, or M)
    
    Returns:
        The row index where the checker was placed, or -1 if column is full
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    
    return -1  # Column is full


def check_win(board, row, col, checker):
    """
    Check if the last placed checker results in a win.
    Check horizontally, vertically, and diagonally.
    
    Args:
        board: The game board (2D list)
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if the player won, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
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


def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are WIN_LENGTH checkers in a row in the specified direction.
    
    Args:
        board: The game board (2D list)
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
        row_delta: The change in row for each step in the direction
        col_delta: The change in column for each step in the direction
    
    Returns:
        True if WIN_LENGTH checkers are found in a row, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    count = 1  # Count the current checker
    
    # Check in the positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in the negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def play_game():
    """
    Main game loop. Controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get current player's checker
        current_checker = PLAYER_CHECKERS[current_player_index]
        
        # Get valid input from current player
        print(f"Player {current_checker}, please enter a column: ", end="")
        col_index = get_valid_input(board)
        
        # Place the checker
        row_index = place_checker(board, col_index, current_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check if the board is full (draw)
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
