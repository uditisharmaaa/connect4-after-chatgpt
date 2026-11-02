import os
import random
import string

# --- Global Constants ---
# Board dimensions
NUM_ROWS = 6
NUM_COLS = 7
# Maximum number of columns supported for labeling (A-Z)
MAX_LABEL_COLS = 26
# Number of players (2 to 5)
NUM_PLAYERS = 2
# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
# Number of checkers needed to win
CONNECT_N = 4

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
        list: A 2D list representing the game board, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(len(board[0])):
        if i < MAX_LABEL_COLS:
            print(f"  {string.ascii_uppercase[i]} ", end="")
        else:
            # Handle cases beyond Z if NUM_COLS > 26 (though assignment limits to 26)
            print(f" {string.ascii_uppercase[i - MAX_LABEL_COLS] + string.ascii_uppercase[0]} ", end="") # Example for AA, AB, etc.
    print()

    # Print the board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for c in range(len(board[r])):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.

    Args:
        col_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if not isinstance(col_char, str) or len(col_char) != 1 or not col_char.isalpha():
        return -1
    col_char = col_char.upper()
    col_index = ord(col_char) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a move to the given column index is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        bool: True if the move is valid (column exists and is not full), False otherwise.
    """
    if not (0 <= col_index < len(board[0])):
        return False  # Column index out of bounds

    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol ('X', 'O', etc.) to place.

    Returns:
        int: The row index where the checker was placed, or -1 if the column was full.
    """
    for r in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return -1  # Column is full (should be caught by is_valid_move already)

def check_win(board, checker, last_row, last_col, connect_n):
    """
    Checks if the last placed checker resulted in a win (4 in a row).

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.
        connect_n (int): The number of checkers needed to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Helper function to check a line in a given direction
    def check_line(dr, dc):
        count = 0
        # Check in one direction
        r, c = last_row, last_col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the opposite direction (excluding the starting point to avoid double counting)
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        return count >= connect_n

    # Check horizontal win
    if check_line(0, 1):
        return True
    # Check vertical win
    if check_line(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if check_line(1, 1):
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if check_line(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw


def main():
    """Main function to run the Connect 4 game."""

    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]  # Get checkers for the specified number of players
    current_player_index = random.randint(0, NUM_PLAYERS - 1) # Randomly choose first player

    game_over = False
    winner = None

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        user_input = input().strip().upper()  # Get and standardize input

        # Input validation loop
        col_index = get_column_index(user_input, NUM_COLS)
        while col_index == -1 or not is_valid_move(board, col_index):
            if col_index == -1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
            else: # Column is full
                print("That column is full. Please choose another column.")
            print(f"Player {current_player_checker}, please enter a column:")
            user_input = input().strip().upper()
            col_index = get_column_index(user_input, NUM_COLS)

        # Place the checker
        last_row_placed = place_checker(board, col_index, current_player_checker)

        # Check for win
        if check_win(board, current_player_checker, last_row_placed, col_index, CONNECT_N):
            winner = current_player_checker
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            game_over = True

        # Switch to the next player if game is not over
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over - print final board and result
    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
