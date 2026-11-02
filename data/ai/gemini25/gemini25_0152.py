import os
import random
import string

# --- Constants (Can be changed for different game configurations) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Between 2 and 5
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
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))

    for r in range(num_rows):
        # Print horizontal line
        print("+---" * num_cols + "+")
        # Print row content
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    # Print bottom horizontal line
    print("+---" * num_cols + "+")


def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its integer index (0).

    Args:
        col_char (str): The column character entered by the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The integer index of the column, or -1 if invalid.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return -1
    col_char = col_char.upper()
    if 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
        return ord(col_char) - ord('A')
    return -1


def is_valid_move(board, col_index):
    """
    Checks if a move to a specific column is valid.

    Args:
        board (list): The game board.
        col_index (int): The integer index of the chosen column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if not (0 <= col_index < len(board[0])):
        return False  # Column index out of bounds
    return board[0][col_index] == " "  # Check if the top row of the column is empty


def drop_checker(board, col_index, player_checker):
    """
    Places a checker in the lowest available space in a given column.

    Args:
        board (list): The game board.
        col_index (int): The integer index of the chosen column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        tuple: (row, col) of where the checker was placed, or (-1, -1) if invalid.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return r, col_index
    return -1, -1  # Should not happen if is_valid_move is checked first


def check_win(board, checker, last_row, last_col, win_condition):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player who just moved.
        last_row (int): The row index where the checker was just placed.
        last_col (int): The column index where the checker was just placed.
        win_condition (int): The number of checkers needed in a row to win.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper to count consecutive checkers in a direction
    def count_direction(r_start, c_start, dr, dc):
        count = 0
        r, c = r_start, c_start
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Horizontal check
    count_h = count_direction(last_row, last_col, 0, -1) + count_direction(last_row, last_col, 0, 1) - 1
    if count_h >= win_condition:
        return True

    # Vertical check
    count_v = count_direction(last_row, last_col, -1, 0) + count_direction(last_row, last_col, 1, 0) - 1
    if count_v >= win_condition:
        return True

    # Diagonal (top-left to bottom-right)
    count_diag1 = count_direction(last_row, last_col, -1, -1) + count_direction(last_row, last_col, 1, 1) - 1
    if count_diag1 >= win_condition:
        return True

    # Diagonal (top-right to bottom-left)
    count_diag2 = count_direction(last_row, last_col, -1, 1) + count_direction(last_row, last_col, 1, -1) - 1
    if count_diag2 >= win_condition:
        return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (game is a draw).

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
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_coords = (-1, -1)  # To store (row, col) of the last placed checker

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        valid_input = False
        while not valid_input:
            user_input = input().strip()
            if not user_input:
                print("Invalid input. Please enter a single letter for the column.")
                continue

            col_index = get_column_index(user_input[0], NUM_COLS)

            if col_index == -1:
                print(f"Invalid column '{user_input[0]}'. Please enter a letter from A to {string.ascii_uppercase[NUM_COLS - 1]}.")
            elif not is_valid_move(board, col_index):
                print(f"Column {user_input[0].upper()} is full. Please choose another column.")
            else:
                valid_input = True

        last_placed_coords = drop_checker(board, col_index, current_player_checker)

        if check_win(board, current_player_checker, last_placed_coords[0], last_placed_coords[1], WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
