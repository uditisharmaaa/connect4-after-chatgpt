import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for letter labels)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
WIN_CONDITION = 4  # Number of consecutive checkers to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# A list of checkers for the active players
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

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
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"  {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board with separators
    for row in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for col in range(len(board[0])):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

def get_player_input(current_player_checker):
    """
    Prompts the current player for their move and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not column_input.isalpha() or len(column_input) != 1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue

            col_index = ord(column_input) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except Exception:
            print("Invalid input. Please try again.")

def place_checker(board, col_index, checker):
    """
    Places the player's checker in the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is to be placed.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    # Iterate from the bottom row upwards
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True, row, col_index  # Return True and the position where checker was placed
    return False, -1, -1 # Return False if column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Store board dimensions for easier access
    rows = NUM_ROWS
    cols = NUM_COLS

    # Check horizontal
    # Count consecutive checkers to the left
    count = 0
    for c in range(max(0, last_col - (WIN_CONDITION - 1)), min(cols, last_col + WIN_CONDITION)):
        if c >= 0 and c < cols and board[last_row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0  # Reset count if consecutive checkers are broken

    # Check vertical
    # Only need to check downwards from the last placed checker
    count = 0
    for r in range(last_row, min(rows, last_row + WIN_CONDITION)):
        if r >= 0 and r < rows and board[r][last_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonals (top-left to bottom-right)
    # Start checking from the potential start of a WIN_CONDITION sequence
    for i in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        count = 0
        for j in range(WIN_CONDITION):
            r, c = last_row + i + j, last_col + i + j
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0

    # Check diagonals (bottom-left to top-right)
    # Start checking from the potential start of a WIN_CONDITION sequence
    for i in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        count = 0
        for j in range(WIN_CONDITION):
            r, c = last_row - i + j, last_col + i - j
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if ' ' in row:
            return False  # If any empty space is found, it's not a draw yet
    return True  # All spaces are filled

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, checks for wins and draws.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = ACTIVE_CHECKERS[current_player_index]
        print_board(board)

        col_input_valid = False
        while not col_input_valid:
            col_index = get_player_input(current_player_checker)
            
            # Place the checker
            successfully_placed, last_row, last_col = place_checker(board, col_index, current_player_checker)
            
            if successfully_placed:
                col_input_valid = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # The turn is not lost, player is asked for valid input again

        # After placing the checker, check for a win
        if check_win(board, current_player_checker, last_row, last_col):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Main Game Execution ---
if __name__ == "__main__":
    play_game()
