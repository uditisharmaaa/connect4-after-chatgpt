import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

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
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"  {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board content
    for row_index in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()
    
    # Print the bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def is_valid_column_input(col_input, num_cols):
    """
    Validates the user's column input.

    Args:
        col_input (str): The raw input from the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index if valid, otherwise None.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return None
    
    col_input = col_input.upper()
    
    if 'A' <= col_input <= chr(ord('A') + num_cols - 1):
        return ord(col_input) - ord('A')
    return None

def get_next_available_row(board, col):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col (int): The 0-based column index.

    Returns:
        int or None: The 0-based row index if space is available, otherwise None.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, col, checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-based column index.
        checker (str): The checker symbol ("X", "O", etc.).

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    row = get_next_available_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_win(board, checker):
    """
    Checks if the given checker has achieved a win condition.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        print(f"Player {current_checker}, please enter a column: ", end="")

        valid_turn = False
        while not valid_turn:
            user_input = input().strip()
            col_index = is_valid_column_input(user_input, NUM_COLS)

            if col_index is None:
                print("Invalid input. Please enter a single letter (e.g., A, B, C): ", end="")
            elif get_next_available_row(board, col_index) is None:
                print("Column is full. Please choose another column: ", end="")
            else:
                valid_turn = True
        
        # Place the checker
        place_checker(board, col_index, current_checker)
        
        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
