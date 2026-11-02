import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Utility Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_column_letter(col_index):
    """Converts a column index (0-based) to its corresponding uppercase letter."""
    return chr(ord('A') + col_index)


def get_column_index(col_letter):
    """Converts an uppercase column letter to its corresponding index (0-based)."""
    return ord(col_letter.upper()) - ord('A')


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates and returns an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {get_column_letter(i)} ", end=" ")
    print()

    # Print board content
    for r in range(len(board)):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_available_row(board, col):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col (int): The column index to check.

    Returns:
        int or None: The row index where a checker can be placed, or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col] == ' ':
            return r
    return None


def place_checker(board, col, checker):
    """
    Places a checker in the specified column at the lowest available spot.

    Args:
        board (list): The game board.
        col (int): The column index where the checker should be placed.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was successfully placed, False if the column was full.
    """
    row = get_available_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False


def is_board_full(board):
    """
    Checks if the game board is completely full (resulting in a draw).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for c in range(len(board[0])):
        if board[0][c] == ' ':  # Check only the top row
            return False
    return True


# --- Win Condition Functions ---
def check_win(board, checker):
    """
    Checks if the given checker has won the game.
    Checks horizontally, vertically, and diagonally.

    Args:
        board (list): The game board.
        checker (str): The checker symbol ('X', 'O', etc.) to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (positive slope)
    for r in range(num_rows - (WIN_SEQUENCE_LENGTH - 1)):
        for c in range(num_cols - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (negative slope)
    for r in range(WIN_SEQUENCE_LENGTH - 1, num_rows):
        for c in range(num_cols - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False


# --- Game Flow Functions ---
def get_player_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The valid 0-based column index.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = get_column_index(user_input)

            if not (0 <= col_index < NUM_COLS):
                print(f"Column '{user_input}' is out of board range. Please choose a column from A to {get_column_letter(NUM_COLS - 1)}.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")


def game_loop():
    """Main game loop for Connect 4."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)

        print(f"Player {current_player_checker}, it's your turn.")

        valid_turn = False
        while not valid_turn:
            col_index = get_player_input(current_player_checker)

            if place_checker(board, col_index, current_player_checker):
                valid_turn = True
            else:
                print(f"Column {get_column_letter(col_index)} is full. Please choose another column.")
                # The turn is not lost, player is asked again

        print_board(board) # Print board after successful placement

        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif is_board_full(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Initializes and starts the Connect 4 game."""
    print("Welcome to Connect 4!")
    print(f"Board Dimensions: {NUM_ROWS} rows x {NUM_COLS} columns")
    print(f"Number of Players: {NUM_PLAYERS}")
    print(f"Player Checkers: {', '.join(CHECKERS)}")
    print(f"Win Condition: {WIN_SEQUENCE_LENGTH} in a row")
    input("Press Enter to start the game...")
    game_loop()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
