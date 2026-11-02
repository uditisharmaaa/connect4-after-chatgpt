import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for A-Z labeling)
NUM_PLAYERS = 2  # Number of players (2 to 5)
WIN_CONDITION = 4  # Number of checkers in a row needed to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# Map column letters (A, B, C...) to their numerical index (0, 1, 2...)
COLUMN_LABELS = {chr(65 + i): i for i in range(NUM_COLS)}
# Reverse map for printing board headers
INDEX_TO_LABEL = {i: chr(65 + i) for i in range(NUM_COLS)}


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
        board.append([' '] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the current game board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{INDEX_TO_LABEL[i]}   ", end="")
    print()

    # Print the board content
    for r_idx, row in enumerate(board):
        print("+---" * len(row) + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * len(board[0]) + "+")


def is_valid_column_input(col_input):
    """
    Checks if the user's column input is valid (a single uppercase letter within bounds).

    Args:
        col_input (str): The raw string input from the user.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    return col_input.upper() in COLUMN_LABELS


def get_column_index(col_input):
    """
    Converts a valid column letter input to its numerical index.

    Args:
        col_input (str): The valid column letter (e.g., 'A', 'B').

    Returns:
        int: The numerical index of the column.
    """
    return COLUMN_LABELS[col_input.upper()]


def is_column_full(board, col_index):
    """
    Checks if a given column is completely filled with checkers.

    Args:
        board (list): The game board.
        col_index (int): The numerical index of the column to check.

    Returns:
        bool: True if the column is full, False otherwise.
    """
    # A column is full if its top-most row (row 0) is not empty
    return board[0][col_index] != ' '


def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The numerical index of the column to drop the checker into.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
    """
    # Iterate from the bottom up to find the first empty spot
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the current player has won the game by connecting WIN_CONDITION checkers
    horizontally, vertically, or diagonally.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal win
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical win
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal win (bottom-left to top-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal win (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
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
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)  # Randomly choose first player

    game_over = False
    winner = None

    while not game_over:
        current_checker = players[current_player_idx]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get valid input from the current player
        while True:
            col_input = input().upper()

            if not is_valid_column_input(col_input):
                print("Invalid column. Please enter a letter from A to "
                      f"{INDEX_TO_LABEL[NUM_COLS - 1]}.")
                continue

            col_index = get_column_index(col_input)

            if is_column_full(board, col_index):
                # The turn is NOT lost according to the assignment, player is asked again.
                print(f"Column {col_input} is full. Please choose another column.")
                continue
            break  # Valid input and column not full, exit loop

        # Drop the checker
        drop_checker(board, col_index, current_checker)

        # Check for win
        if check_win(board, current_checker):
            winner = current_checker
            game_over = True
        # Check for draw
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game Over
    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
