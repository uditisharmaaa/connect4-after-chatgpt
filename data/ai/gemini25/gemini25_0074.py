import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Maximum 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

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
        list[list[str]]: A 2D list representing the board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list[list[str]]): The 2D list representing the current board state.
    """
    clear_screen()  # Clear screen before printing
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(num_cols):
        print(f"   {chr(ord('A') + col_index)}", end="")
    print("\n" + "  " + "+---" * num_cols + "+")

    # Print board rows
    for row in board:
        print("  ", end="")
        for cell in row:
            print(f"| {cell} ", end="")
        print("|\n" + "  " + "+---" * num_cols + "+")

def get_column_from_input(prompt, num_cols):
    """
    Prompts the user for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.
        num_cols (int): The total number of columns available.

    Returns:
        int or None: The 0-indexed column number if valid, None otherwise.
    """
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + num_cols - 1):
            return ord(user_input) - ord('A')  # Convert 'A' to 0, 'B' to 1, etc.
        else:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")

def place_checker(board, col_index, checker):
    """
    Places a checker in the specified column at the lowest available row.

    Args:
        board (list[list[str]]): The current board state.
        col_index (int): The 0-indexed column number to place the checker.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    num_rows = len(board)
    for row in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has formed a Connect 4 (horizontal, vertical, or diagonal).

    Args:
        board (list[list[str]]): The current board state.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(num_rows - 3):
        for c in range(num_cols):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals (bottom-left to top-right)
    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check negatively sloped diagonals (top-left to bottom-right)
    for r in range(3, num_rows):
        for c in range(num_cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list[list[str]]): The current board state.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False  # An empty space is found, not a draw yet
    return True  # No empty spaces, it's a draw

def main():
    """Main function to run the Connect 4 game."""

    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Get checkers for the number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    # Game loop
    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        col_input_valid = False
        while not col_input_valid:
            col_index = get_column_from_input(f"Player {current_checker}'s turn: ", NUM_COLS)
            
            if col_index is not None:
                if place_checker(board, col_index, current_checker):
                    col_input_valid = True
                else:
                    print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # If col_index is None, get_column_from_input already printed an error message, loop continues.

        # After placing, print the board again to show the update
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
