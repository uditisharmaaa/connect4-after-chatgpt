import os
import random
import string

# Constants for board dimensions and players
ROWS = 6          # Number of rows in the board
COLUMNS = 7       # Number of columns in the board (max 26 due to labeling with letters)
NUM_PLAYERS = 2   # Number of players (between 2 and 5)

# Player checkers in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row needed to win
WIN_COUNT = 4

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """
    Create a new board filled with spaces.

    Args:
        rows (int): Number of rows.
        columns (int): Number of columns.

    Returns:
        list: 2D list representing the board.
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Print the current state of the board to the terminal.

    Args:
        board (list): 2D list representing the board.
    """
    # Print column labels (letters A-G or more if bigger board)
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    # Print rows with borders
    row_count = len(board)
    col_count = len(board[0])
    hline = "+---" * col_count + "+"
    for r in range(row_count):
        print(hline)
        row_cells = []
        for c in range(col_count):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(hline)

def is_valid_column(input_str, columns):
    """
    Validate that the input is a single uppercase letter within board columns.

    Args:
        input_str (str): User input string.
        columns (int): Number of columns.

    Returns:
        bool: True if input valid column letter, False otherwise.
    """
    if len(input_str) != 1:
        return False
    if input_str not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column_index(column_letter):
    """
    Convert a column letter to its 0-based index.

    Args:
        column_letter (str): Single uppercase letter.

    Returns:
        int: Column index (0-based).
    """
    return ord(column_letter) - ord('A')

def place_checker(board, column_index, checker):
    """
    Place a checker into the column if possible.

    Args:
        board (list): 2D list representing the board.
        column_index (int): The column number (0-based).
        checker (str): Player's checker symbol.

    Returns:
        bool: True if placed successfully, False if column full.
    """
    # Starting from bottom row upwards, find the first empty slot
    for row in range(len(board)-1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return True
    return False  # Column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    """
    Check how many consecutive checkers are in a particular direction.

    Args:
        board (list): 2D list representing the board.
        start_row (int): Starting row index.
        start_col (int): Starting column index.
        delta_row (int): Row increment direction.
        delta_col (int): Column increment direction.
        checker (str): Player's checker symbol.

    Returns:
        int: Number of consecutive checkers including the start position.
    """
    count = 0
    row = start_row
    col = start_col
    rows = len(board)
    cols = len(board[0])

    while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col

    return count

def check_win(board, checker):
    """
    Check the board if the player with 'checker' has won.

    Args:
        board (list): 2D list representing the board.
        checker (str): Player's checker symbol.

    Returns:
        bool: True if player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                # Check all directions: horizontal, vertical, diagonal /
                # and diagonal \
                # We count consecutive checkers in both directions for each line

                # Horizontal (left to right)
                hor_count = (check_direction(board, r, c, 0, 1, checker) +
                             check_direction(board, r, c-1, 0, -1, checker) - 1)
                if hor_count >= WIN_COUNT:
                    return True

                # Vertical (top to bottom)
                vert_count = (check_direction(board, r, c, 1, 0, checker) +
                              check_direction(board, r-1, c, -1, 0, checker) - 1)
                if vert_count >= WIN_COUNT:
                    return True

                # Diagonal \ (top-left to bottom-right)
                diag1_count = (check_direction(board, r, c, 1, 1, checker) +
                               check_direction(board, r-1, c-1, -1, -1, checker) - 1)
                if diag1_count >= WIN_COUNT:
                    return True

                # Diagonal / (bottom-left to top-right)
                diag2_count = (check_direction(board, r, c, -1, 1, checker) +
                               check_direction(board, r+1, c-1, 1, -1, checker) - 1)
                if diag2_count >= WIN_COUNT:
                    return True
    return False

def board_full(board):
    """
    Check if the board is completely full (no empty spaces).

    Args:
        board (list): 2D list representing the board.

    Returns:
        bool: True if board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Create and initialize the game board
    board = create_board(ROWS, COLUMNS)

    # Select a random starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Used player checkers in order, depends on number of players
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input validation loop for player's column choice
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, COLUMNS):
                # Invalid input, not a valid column letter
                print("Invalid input. Please enter a letter corresponding to a valid column (e.g. A-G).")
                continue

            col_index = get_column_index(user_input)
            # Check if column full before placing
            if board[0][col_index] != " ":
                # Column full - player loses turn
                print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
                # pause before losing turn so player can see message
                input("Press Enter to continue...")
                break  # Exit input loop but no checker placed

            # Place checker
            placed = place_checker(board, col_index, current_checker)
            if placed:
                break
            else:
                # Should not reach here because we already checked top cell.
                print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
                input("Press Enter to continue...")
                break

        # Check for win if checker was placed
        if placed:
            if check_win(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                return

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            return

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
