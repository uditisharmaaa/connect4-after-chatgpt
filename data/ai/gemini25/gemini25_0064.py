import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Global Variables ---
board = []


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
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(current_board):
    """
    Prints the Connect 4 board to the console.

    Args:
        current_board (list): The 2D list representing the game board.
    """
    clear_screen()
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {current_board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")


def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.

    Returns:
        int: The 0-indexed column number if the input is valid, otherwise asks again.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
                print("Invalid column. Please enter a single letter corresponding to a column (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print("Column out of board range. Please try again.")
                continue

            # Check if the column is full
            if board[0][col_index] != " ":
                print("Column is full. Please choose another column.")
                continue

            return col_index
        except Exception:
            print("Invalid input. Please enter a letter.")


def drop_checker(col_index, current_player_checker):
    """
    Drops the checker into the specified column.

    Args:
        col_index (int): The 0-indexed column number.
        current_player_checker (str): The checker of the current player.

    Returns:
        tuple: (row_placed, col_placed) where the checker was placed, or None if unsuccessful.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = current_player_checker
            return r, col_index
    return None  # Should not happen if column full check is done before


def check_win(row, col, checker):
    """
    Checks if the last placed checker results in a win.

    Args:
        row (int): The row where the checker was placed.
        col (int): The column where the checker was placed.
        checker (str): The checker of the current player.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(max(0, col - WIN_CONDITION + 1), min(NUM_COLS - 1, col + WIN_CONDITION - 1) + 1):
        if 0 <= c < NUM_COLS and board[row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r_check in range(max(0, row - WIN_CONDITION + 1), min(NUM_ROWS - 1, row + WIN_CONDITION - 1) + 1):
        if 0 <= r_check < NUM_ROWS and board[r_check][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    start_r = row - (WIN_CONDITION - 1)
    start_c = col - (WIN_CONDITION - 1)
    for i in range(WIN_CONDITION * 2 - 1): # Iterate enough times to cover all diagonals
        r_check = start_r + i
        c_check = start_c + i
        if 0 <= r_check < NUM_ROWS and 0 <= c_check < NUM_COLS and board[r_check][c_check] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (bottom-left to top-right)
    count = 0
    start_r = row + (WIN_CONDITION - 1)
    start_c = col - (WIN_CONDITION - 1)
    for i in range(WIN_CONDITION * 2 - 1): # Iterate enough times to cover all diagonals
        r_check = start_r - i
        c_check = start_c + i
        if 0 <= r_check < NUM_ROWS and 0 <= c_check < NUM_COLS and board[r_check][c_check] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    return False


def check_draw():
    """
    Checks if the board is completely filled, indicating a draw.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw


def play_game():
    """
    Main function to run the Connect 4 game.
    """
    global board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker)
        row_placed, col_placed = drop_checker(col_index, current_player_checker)

        if check_win(row_placed, col_placed, current_player_checker):
            print_board(board)
            winner = current_player_checker
            game_over = True
        elif check_draw():
            print_board(board)
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game end
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


# --- Main execution ---
if __name__ == "__main__":
    play_game()
