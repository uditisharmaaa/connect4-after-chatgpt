import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
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
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board rows
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()

        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()

    # Print bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its corresponding integer index.

    Args:
        column_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(column_char) != 1 or not column_char.isalpha():
        return -1
    index = ord(column_char.upper()) - ord('A')
    if 0 <= index < num_cols:
        return index
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a move to the specified column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the chosen column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if not (0 <= col_index < len(board[0])):
        return False  # Column index out of bounds
    return board[0][col_index] == " "  # Check if the top row of the column is empty

def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the chosen column.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Column is full (should have been caught by is_valid_move)

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, num_cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
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
    num_cols = len(board[0])
    for c in range(num_cols):
        if board[0][c] == " ":  # If any space in the top row is empty, game is not a draw
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    num_cols = len(board[0])
    num_players_actual = len(PLAYER_CHECKERS)

    # Randomly choose the first player
    current_player_index = random.randint(0, num_players_actual - 1)
    current_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        column_input = input().strip().upper()
        col_index = get_column_index(column_input, num_cols)

        if col_index == -1:
            print("Invalid column. Please enter a letter from A to", string.ascii_uppercase[num_cols - 1])
            # Player does not lose turn for invalid input
            continue

        if not is_valid_move(board, col_index):
            print("Column is full. Please choose another column.")
            # Player does not lose turn for invalid input
            continue

        place_checker(board, col_index, current_checker)

        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % num_players_actual
            current_checker = PLAYER_CHECKERS[current_player_index]

if __name__ == "__main__":
    main()
