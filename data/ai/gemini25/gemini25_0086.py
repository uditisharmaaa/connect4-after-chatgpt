import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current game board.
    """
    num_cols = len(board[0])
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print the board with separators
    for row in board:
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print the bottom separator
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.

    Args:
        col_char (str): The column character entered by the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return -1
    
    col_char = col_char.upper()
    
    if 'A' <= col_char <= chr(ord('A') + num_cols - 1):
        return ord(col_char) - ord('A')
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a chosen column is valid for placing a checker.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the chosen column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    num_cols = len(board[0])
    if not (0 <= col_index < num_cols):
        return False  # Column index out of bounds

    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol for the current player.

    Returns:
        int: The row index where the checker was placed, or -1 if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return -1 # Column is full (though this should be caught by is_valid_move)

def check_win(board, checker):
    """
    Checks if the given player (checker) has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal wins (bottom-left to top-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal wins (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (game is a draw).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Manages the main Connect 4 game flow.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randrange(NUM_PLAYERS)
    
    game_over = False
    
    while not game_over:
        clear_screen()
        print_board(board)
        
        current_checker = PLAYER_CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column: ", end="")
        
        col_input = sys.stdin.readline().strip() # Use sys.stdin.readline for consistency in some environments
        col_index = get_column_index(col_input, NUM_COLS)

        if col_index == -1:
            print("Invalid input. Please enter a valid column letter (e.g., A, B).")
            # Player does not lose turn
            continue
        
        if not is_valid_move(board, col_index):
            print("That column is full. Please choose another column.")
            # Player does not lose turn
            continue

        drop_checker(board, col_index, current_checker)
        
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_game()
