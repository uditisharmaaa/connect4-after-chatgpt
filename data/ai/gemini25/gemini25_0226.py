import os
import random
import string

# --- Global Constants ---
# Board dimensions (can be changed for different board sizes)
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z

# Number of players (can be changed, between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players (up to 5 players)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers needed to win
WIN_CONDITION = 4

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    column_labels = string.ascii_uppercase[:num_cols]
    print("  " + "   ".join(column_labels))

    # Print the board with separators
    for r in range(num_rows):
        print("+" + "---+" * num_cols)
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * num_cols)

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its corresponding 0-based index.

    Args:
        column_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index if valid, otherwise None.
    """
    if len(column_char) == 1 and 'A' <= column_char <= string.ascii_uppercase[num_cols - 1]:
        return ord(column_char) - ord('A')
    return None

def is_valid_move(board, col_index):
    """
    Checks if a chosen column is valid for placing a checker.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the chosen column.

    Returns:
        bool: True if the column is valid and not full, False otherwise.
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
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        int: The row index where the checker was placed, or -1 if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return -1  # Column is full (should be caught by is_valid_move, but good for robustness)

def check_win(board, row, col, checker):
    """
    Checks if the last placed checker results in a win (4 in a row).

    Args:
        board (list): The game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol that was just placed.

    Returns:
        bool: True if there's a win, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Directions for checking (horizontal, vertical, diagonal)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]

    for dr, dc in directions:
        count = 1  # Count of consecutive checkers, starting with the one just placed

        # Check in one direction
        for i in range(1, WIN_CONDITION):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
            else:
                break

        # Check in the opposite direction
        for i in range(1, WIN_CONDITION):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
            else:
                break

        if count >= WIN_CONDITION:
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
    num_cols = len(board[0])
    for c in range(num_cols):
        if board[0][c] == " ":  # If the top row of any column is empty, not a draw
            return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Manages the Connect 4 game flow.
    Initializes the board, handles turns, validates input, checks for wins/draws.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]

    game_over = False
    winning_player = None

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Input validation loop
        while True:
            try:
                user_input = input().strip().upper()
                col_index = get_column_index(user_input, NUM_COLS)

                if col_index is None:
                    print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
                elif not is_valid_move(board, col_index):
                    # This implies the column is full or out of bounds (which get_column_index should catch)
                    # For a full column, is_valid_move will return False
                    print(f"Column {user_input} is full. Please choose another column.")
                else:
                    break  # Valid input and valid move, exit inner loop

            except EOFError: # Handles Ctrl+D gracefully
                print("\nGame interrupted. Exiting.")
                return
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

        # Place the checker
        placed_row = drop_checker(board, col_index, current_checker)

        # Check for win
        if check_win(board, placed_row, col_index, current_checker):
            print_board(board) # Print final board with winning move
            winning_player = current_checker
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            print_board(board) # Print final board for draw
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player_index]

    # End of game messages
    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("The game is a draw!")

# --- Entry Point ---
if __name__ == "__main__":
    play_game()
