import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- HELPER FUNCTIONS ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

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
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(num_cols):
        print(f"{chr(ord('A') + col_index)}   ", end="")
    print("\n" + "+---" * num_cols + "+")

    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n" + "+---" * num_cols + "+")


def get_column_from_input(board, prompt):
    """
    Prompts the player for a column input and validates it.

    Args:
        board (list): The game board.
        prompt (str): The message to display to the player.

    Returns:
        int: The validated column index (0-based).
    """
    num_cols = len(board[0])
    while True:
        col_input = input(prompt).strip().upper()

        if not col_input:
            print("Error: Input cannot be empty. Please enter a column letter.")
            continue

        if len(col_input) != 1:
            print("Error: Please enter a single letter for the column.")
            continue

        col_index = ord(col_input) - ord('A')

        if not (0 <= col_index < num_cols):
            print(f"Error: Column '{col_input}' is out of board range. Please enter a letter from A to {chr(ord('A') + num_cols - 1)}.")
            continue

        if board[0][col_index] != " ":
            print(f"Error: Column '{col_input}' is full. Please choose another column.")
            continue

        return col_index


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        tuple: (row_placed, col_placed) of the checker, or (-1, -1) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return -1, -1  # Should not happen if input validation is correct


def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the current player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Directions for checking (horizontal, vertical, diagonal)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal /
        (1, -1)   # Diagonal \
    ]

    for dr, dc in directions:
        count = 0
        # Check in one direction
        for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
            r, c = last_row + i * dr, last_col + i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0  # Reset count if consecutive checkers are broken
    return False


def check_draw(board):
    """
    Checks if the board is completely full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_cols = len(board[0])
    for col_index in range(num_cols):
        if board[0][col_index] == " ":  # If the top row of any column is empty, game is not a draw
            return False
    return True


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_pos = (-1, -1)  # (row, col) of the last placed checker

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        
        # Display current player and their checker
        sys.stdout.write(f"Player {current_checker}, please enter a column: ")
        sys.stdout.flush()

        # Get and validate column input
        col_index = get_column_from_input(board, "") # Prompt already printed

        # Drop the checker
        row_placed, col_placed = drop_checker(board, col_index, current_checker)
        last_placed_pos = (row_placed, col_placed) # Update last placed position

        # Check for win
        if check_win(board, current_checker, last_placed_pos[0], last_placed_pos[1]):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
