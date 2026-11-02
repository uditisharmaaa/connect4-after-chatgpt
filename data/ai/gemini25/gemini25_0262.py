import os
import random
import string

# --- Global Constants (DO NOT MODIFY FOR SUBMISSION) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win
# Checkers for players. Max 5 players (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board,
              initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board content
    for r in range(num_rows):
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

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A') to its corresponding 0-based index.

    Args:
        column_char (str): The uppercase letter representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= string.ascii_uppercase[NUM_COLS - 1]:
        return ord(column_char) - ord('A')
    return -1

def is_valid_column_input(column_char, num_cols):
    """
    Checks if the user's column input is valid.

    Args:
        column_char (str): The user's input for the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        bool: True if the input is a single uppercase letter within valid range, False otherwise.
    """
    return len(column_char) == 1 and column_char.isupper() and 'A' <= column_char <= string.ascii_uppercase[num_cols - 1]

def get_player_move(current_player_checker, board):
    """
    Prompts the current player for a column choice and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board (list): The game board.

    Returns:
        int: The 0-based index of the chosen column.
    """
    num_cols = len(board[0])
    while True:
        try:
            col_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not is_valid_column_input(col_input, num_cols):
                print(f"Invalid input. Please enter a single uppercase letter from A to {string.ascii_uppercase[num_cols - 1]}.")
                continue

            col_index = get_column_index(col_input)

            # Check if column is full
            if board[0][col_index] != ' ':
                print(f"Column {col_input} is full. Please choose another column.")
                continue

            return col_index
        except IndexError: # Should not happen with validation but good practice
            print("An unexpected error occurred with column selection. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        tuple: A tuple (row_index, col_index) indicating where the checker landed,
               or (-1, -1) if the column was full (though this should be caught earlier).
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return r, col_index
    return -1, -1  # Should not be reached if validation is correct

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a line
    def check_line(r_start, c_start, r_delta, c_delta):
        count = 0
        for i in range(WIN_CONDITION):
            r, c = r_start + i * r_delta, c_start + i * c_delta
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
            else:
                break
        return count == WIN_CONDITION

    # Check horizontal
    # Find the leftmost point of a potential WIN_CONDITION sequence
    for c_offset in range(-WIN_CONDITION + 1, 1): # Example for WIN_CONDITION=4: -3, -2, -1, 0
        if check_line(last_row, last_col + c_offset, 0, 1):
            return True

    # Check vertical
    # Only need to check downwards from the last placed checker
    for r_offset in range(-WIN_CONDITION + 1, 1): # Example for WIN_CONDITION=4: -3, -2, -1, 0
        if check_line(last_row + r_offset, last_col, 1, 0):
            return True

    # Check diagonal (top-left to bottom-right)
    # Find the top-leftmost point of a potential WIN_CONDITION sequence
    for offset in range(-WIN_CONDITION + 1, 1):
        if check_line(last_row + offset, last_col + offset, 1, 1):
            return True

    # Check anti-diagonal (top-right to bottom-left)
    # Find the top-rightmost point of a potential WIN_CONDITION sequence
    for offset in range(-WIN_CONDITION + 1, 1):
        if check_line(last_row + offset, last_col - offset, 1, -1):
            return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False
    return True

# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    clear_screen()
    print_board(board)

    while not game_over:
        current_player_checker = players[current_player_index]

        col_index = get_player_move(current_player_checker, board)

        # Drop the checker
        last_row, last_col = drop_checker(board, col_index, current_player_checker)

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_player_checker, last_row, last_col):
            winner_checker = current_player_checker
            game_over = True
        # Check for draw
        elif check_draw(board):
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
