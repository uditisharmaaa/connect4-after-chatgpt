import os
import random
import string

# --- Global Constants ---
# Board dimensions
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for A-Z column labels

# Player settings
NUM_PLAYERS = 2  # Between 2 and 5 players
# Checkers for players: X, O, V, H, M
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers needed to win
WIN_LENGTH = 4

# Empty cell representation
EMPTY_CELL = " "

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([EMPTY_CELL] * cols)
    return board

def clear_screen():
    """
    Clears the terminal screen.
    Works on Linux/Unix systems (and potentially macOS).
    """
    os.system('clear')

def print_board(board):
    """
    Prints the Connect 4 board to the console with column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear screen before printing the updated board

    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    col_labels = string.ascii_uppercase[:num_cols]
    header = "  " + "   ".join(col_labels)
    print(header)

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_player_input(player_checker, board):
    """
    Prompts the current player for a column input and validates it.
    Repeats until valid input is received.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    valid_cols = string.ascii_uppercase[:num_cols]

    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").upper()

            # Check if input is a single letter
            if not len(col_input) == 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            # Check if the letter is a valid column label
            if col_input not in valid_cols:
                print(f"Invalid column. Please choose a column from {valid_cols[0]} to {valid_cols[-1]}.")
                continue

            col_index = ord(col_input) - ord('A') # Convert letter to 0-indexed column

            # Check if the column is full
            if board[0][col_index] != EMPTY_CELL:
                print(f"Column {col_input} is full. Please choose another column.")
                continue

            return col_index

        except ValueError:
            print("Invalid input. Please enter a letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def drop_checker(board, col_index, checker):
    """
    Drops the player's checker into the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
        int: The row index where the checker was placed, or -1 if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = checker
            return True, r  # Return True and the row where it was placed
    return False, -1 # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win (4 in a row horizontally,
    vertically, or diagonally).

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a given direction
    def count_consecutive(delta_row, delta_col):
        count = 0
        # Check in one direction
        r, c = last_row, last_col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        # Check in the opposite direction (don't double count the starting checker)
        r, c = last_row - delta_row, last_col - delta_col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r -= delta_row
            c -= delta_col
        return count

    # Check horizontal win
    if count_consecutive(0, 1) >= WIN_LENGTH:
        return True

    # Check vertical win
    if count_consecutive(1, 0) >= WIN_LENGTH:
        return True

    # Check positive diagonal win (bottom-left to top-right)
    if count_consecutive(1, 1) >= WIN_LENGTH:
        return True

    # Check negative diagonal win (top-left to bottom-right)
    if count_consecutive(1, -1) >= WIN_LENGTH:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == EMPTY_CELL:
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles player turns, checks for wins/draws.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = len(PLAYER_CHECKERS)
    current_player_index = random.randint(0, num_players - 1)  # Randomly select first player

    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        # Get valid column input from the player
        col_to_drop = get_player_input(current_checker, board)

        # Drop the checker and get the row where it landed
        successfully_dropped, row_placed = drop_checker(board, col_to_drop, current_checker)

        # This part of the code should only be reached with a valid move now,
        # as get_player_input already handles full columns.
        # However, it's good practice to keep the check for robustness if get_player_input
        # ever changes or is bypassed.
        if not successfully_dropped:
            print(f"Error: Column {string.ascii_uppercase[col_to_drop]} should not have been full. Skipping turn.")
            # Do not change player index if the move was somehow invalid here
            continue

        # Check for a win after dropping the checker
        if check_win(board, current_checker, row_placed, col_to_drop):
            print_board(board)
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % num_players

    # Game ended, print results
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

# --- Main execution ---
if __name__ == "__main__":
    play_game()
