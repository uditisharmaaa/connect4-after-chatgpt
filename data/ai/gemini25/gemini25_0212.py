import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


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
    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")


def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed valid column number chosen by the player.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., A).")
                continue

            # Convert column letter to 0-indexed integer
            col_index = ord(user_input[0]) - ord('A')

            if 0 <= col_index < num_cols and len(user_input) == 1:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and "
                      f"{chr(ord('A') + num_cols - 1)}.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single column letter (e.g., A).")


def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol ("X", "O", etc.).

    Returns:
        bool: True if the checker was successfully placed, False if the column was full.
        int: The row index where the checker was placed, or -1 if placement failed.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r
    return False, -1  # Column is full


def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[last_row][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(num_rows):
        if board[r][last_col] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check positive slope diagonal (bottom-left to top-right)
    # Start checking from the most bottom-left point for the diagonal containing (last_row, last_col)
    row_start = last_row + last_col
    col_start = 0
    if row_start >= num_rows:
        col_start = row_start - (num_rows - 1)
        row_start = num_rows - 1

    count = 0
    r, c = row_start, col_start
    while r >= 0 and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    # Check negative slope diagonal (top-left to bottom-right)
    # Start checking from the most top-left point for the diagonal containing (last_row, last_col)
    row_start = last_row - last_col
    col_start = 0
    if row_start < 0:
        col_start = -row_start
        row_start = 0

    count = 0
    r, c = row_start, col_start
    while r < num_rows and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r += 1
        c += 1

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (draw condition).

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
                return False  # An empty space found, not a draw yet
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = len(PLAYER_CHECKERS)

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_choice = get_column_input(current_player_checker, NUM_COLS)
            
            # Attempt to drop the checker
            placed, row_index = drop_checker(board, col_choice, current_player_checker)

            if placed:
                last_placed_row = row_index
                last_placed_col = col_choice
                valid_turn = True
            else:
                print("Column is full! Please choose another column.")

        # After a valid turn, check for win or draw
        if check_win(board, current_player_checker, last_placed_row, last_placed_col):
            print_board(board)  # Show final board with winning move
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)  # Show final board
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
