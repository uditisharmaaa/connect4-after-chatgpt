import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


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
    Print the board in the required format.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col):^3}", end=" ")
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
        
        # Print border after each row
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def is_valid_input(col_input, cols):
    """
    Validate the column input from the player.
    
    Args:
        col_input: The input string from the player
        cols: Number of columns in the board
    
    Returns:
        A tuple (is_valid, col_index) where is_valid is True if valid,
        and col_index is the 0-indexed column number
    """
    # Check if input is a single character
    if len(col_input) != 1:
        return False, -1
    
    # Check if input is a letter
    if not col_input.isalpha():
        return False, -1
    
    # Convert to uppercase and get column index
    col_index = ord(col_input.upper()) - ord('A')
    
    # Check if column index is within bounds
    if col_index < 0 or col_index >= cols:
        return False, -1
    
    return True, col_index


def is_column_full(board, col):
    """
    Check if a column is completely full.
    
    Args:
        board: The current game board
        col: The column index to check
    
    Returns:
        True if the column is full, False otherwise
    """
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col: The column index where the checker should be placed
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


def check_horizontal_win(board, checker):
    """
    Check if there's a horizontal win for the given checker.
    
    Args:
        board: The current game board
        checker: The checker symbol to check for
    
    Returns:
        True if there's a horizontal win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, checker):
    """
    Check if there's a vertical win for the given checker.
    
    Args:
        board: The current game board
        checker: The checker symbol to check for
    
    Returns:
        True if there's a vertical win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, checker):
    """
    Check if there's a diagonal win for the given checker.
    Checks both directions: top-left to bottom-right and top-right to bottom-left.
    
    Args:
        board: The current game board
        checker: The checker symbol to check for
    
    Returns:
        True if there's a diagonal win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check top-left to bottom-right diagonals
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check top-right to bottom-left diagonals
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the player with the given checker has won.
    
    Args:
        board: The current game board
        checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The current game board
    
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
    print(f"Player {CHECKERS[current_player]} starts!")
    input("Press Enter to begin...")
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get valid input from current player
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip()
            valid, col_index = is_valid_input(col_input, COLS)
            
            if not valid:
                print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")
                continue
            
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        checker = CHECKERS[current_player]
        place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The board is full. It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
