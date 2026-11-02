import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the board in a formatted way with column labels.
    
    Args:
        board: The 2D list representing the board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print board rows
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def get_next_available_row(board, col):
    """
    Get the next available row in a column where a checker can be placed.
    
    Args:
        board: The 2D list representing the board
        col: The column index (0-based)
    
    Returns:
        The row index (0-based) where the checker should be placed,
        or -1 if the column is full
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def is_valid_input(input_str, cols):
    """
    Validate the user input.
    
    Args:
        input_str: The user input string
        cols: Number of columns in the board
    
    Returns:
        True if the input is valid, False otherwise
    """
    if len(input_str) != 1:
        return False
    
    if not input_str.isupper():
        return False
    
    col_index = ord(input_str) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_input(cols):
    """
    Get and validate the column input from the user.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based)
    """
    while True:
        col_input = input(f"Please enter a column (A-{chr(ord('A') + cols - 1)}): ").strip().upper()
        
        if not is_valid_input(col_input, cols):
            print("Invalid input. Please try again.")
            continue
        
        col_index = ord(col_input) - ord('A')
        return col_index


def place_checker(board, col, checker, cols):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the board
        col: The column index (0-based)
        checker: The checker character (e.g., "X", "O")
        cols: Number of columns in the board
    
    Returns:
        True if the checker was placed successfully, False if the column is full
    """
    row = get_next_available_row(board, col)
    
    if row == -1:
        print("Column is full. Please choose another column.")
        return False
    
    board[row][col] = checker
    return True


def check_winner(board, rows, cols, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: The checker character to check for (e.g., "X", "O")
    
    Returns:
        True if the checker has won, False otherwise
    """
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board, rows, cols):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D list representing the board
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


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Get the checkers for each player
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board, COLS)
    
    # Main game loop
    game_over = False
    
    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column input
        while True:
            col = get_column_input(COLS)
            
            # Try to place the checker
            if place_checker(board, col, current_checker, COLS):
                break
        
        # Print the updated board
        print_board(board, COLS)
        
        # Check for a win
        if check_winner(board, ROWS, COLS, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        
        # Check for a draw
        elif is_board_full(board, ROWS, COLS):
            print("Draw!")
            game_over = True
        
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
