import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


# --- Game Board Functions ---

def create_board():
    """
    Creates and returns an empty Connect 4 game board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(NUM_ROWS):
        board.append([" "] * NUM_COLS)
    return board


def print_board(board):
    """
    Clears the screen and prints the current state of the game board.
    Includes column labels and separators.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))

    # Print top border
    print("+" + "---+".join(["-"] * NUM_COLS) + "+")

    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+".join(["-"] * NUM_COLS) + "+")


def is_valid_column_input(column_input):
    """
    Checks if the user's column input is a single uppercase letter
    corresponding to a valid column on the board.
    """
    if not isinstance(column_input, str) or len(column_input) != 1:
        return False
    return 'A' <= column_input <= COLUMN_LABELS[-1]


def get_column_index(column_label):
    """
    Converts a column letter label (e.g., 'A') to its corresponding
    integer index (e.g., 0).
    Assumes the input label is valid.
    """
    return ord(column_label) - ord('A')


def is_column_full(board, col_index):
    """
    Checks if the specified column is completely filled with checkers.
    """
    return board[0][col_index] != " "


def drop_checker(board, col_index, checker):
    """
    Drops the specified checker into the given column.
    Places the checker in the lowest available space.
    Returns the row index where the checker was placed, or -1 if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1  # Column is full (should be caught by is_column_full before this)


# --- Win Condition Functions ---

def check_win(board, row, col, checker):
    """
    Checks if the given checker has formed a winning line (4 in a row)
    after being placed at (row, col).
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontally
    if check_horizontal_win(board, row, col, checker):
        return True
    # Check vertically
    if check_vertical_win(board, row, col, checker):
        return True
    # Check diagonally (positive slope /)
    if check_diagonal_positive_win(board, row, col, checker):
        return True
    # Check diagonally (negative slope \)
    if check_diagonal_negative_win(board, row, col, checker):
        return True
    return False


def check_horizontal_win(board, row, col, checker):
    """Checks for a horizontal win around the given position."""
    count = 0
    # Check to the left
    for c in range(max(0, col - (WIN_CONDITION - 1)), col + 1):
        current_count = 0
        for i in range(WIN_CONDITION):
            if c + i < NUM_COLS and board[row][c + i] == checker:
                current_count += 1
            else:
                break
        if current_count == WIN_CONDITION:
            return True
    return False


def check_vertical_win(board, row, col, checker):
    """Checks for a vertical win around the given position."""
    count = 0
    # Check downwards only
    for r in range(max(0, row - (WIN_CONDITION - 1)), row + 1):
        current_count = 0
        for i in range(WIN_CONDITION):
            if r + i < NUM_ROWS and board[r + i][col] == checker:
                current_count += 1
            else:
                break
        if current_count == WIN_CONDITION:
            return True
    return False


def check_diagonal_positive_win(board, row, col, checker):
    """Checks for a diagonal win with a positive slope (/) around the given position."""
    # Find the start of the potential diagonal line (bottom-left to top-right)
    # The 'origin' of the diagonal (row_start, col_start) is the bottom-most, left-most point
    # that could potentially start a WIN_CONDITION length diagonal ending at (row, col)
    for i in range(WIN_CONDITION):
        r_start = row + i
        c_start = col - i

        if 0 <= r_start < NUM_ROWS and 0 <= c_start < NUM_COLS:
            # Check the diagonal starting from (r_start, c_start)
            current_count = 0
            for k in range(WIN_CONDITION):
                r_check = r_start - k
                c_check = c_start + k
                if 0 <= r_check < NUM_ROWS and 0 <= c_check < NUM_COLS and board[r_check][c_check] == checker:
                    current_count += 1
                else:
                    break
            if current_count == WIN_CONDITION:
                return True
    return False


def check_diagonal_negative_win(board, row, col, checker):
    """Checks for a diagonal win with a negative slope (\) around the given position."""
    # Find the start of the potential diagonal line (top-left to bottom-right)
    # The 'origin' of the diagonal (row_start, col_start) is the top-most, left-most point
    # that could potentially start a WIN_CONDITION length diagonal ending at (row, col)
    for i in range(WIN_CONDITION):
        r_start = row - i
        c_start = col - i

        if 0 <= r_start < NUM_ROWS and 0 <= c_start < NUM_COLS:
            # Check the diagonal starting from (r_start, c_start)
            current_count = 0
            for k in range(WIN_CONDITION):
                r_check = r_start + k
                c_check = c_start + k
                if 0 <= r_check < NUM_ROWS and 0 <= c_check < NUM_COLS and board[r_check][c_check] == checker:
                    current_count += 1
                else:
                    break
            if current_count == WIN_CONDITION:
                return True
    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full


# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles player turns, checks for wins/draws.
    """
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get and validate player input
        while True:
            try:
                col_input = input().strip().upper()
                if not is_valid_column_input(col_input):
                    print("Invalid input. Please enter a single letter (e.g., A) within the board range.")
                    continue

                col_index = get_column_index(col_input)

                if is_column_full(board, col_index):
                    print(f"Column {col_input} is full. Please choose another column.")
                else:
                    break  # Valid input and column not full
            except EOFError:
                print("\nExiting game.")
                sys.exit()
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

        # Drop the checker
        row_placed = drop_checker(board, col_index, current_checker)

        # Check for win
        if check_win(board, row_placed, col_index, current_checker):
            winner_checker = current_checker
            game_over = True
        # Check for draw
        elif check_draw(board):
            game_over = True
            winner_checker = "Draw"  # Special value for a draw
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game Over
    print_board(board)  # Print final board state
    if winner_checker == "Draw":
        print("The game is a draw!")
    else:
        print(f"Player {winner_checker} won!")


# --- Program Entry Point ---
if __name__ == "__main__":
    play_connect_4()
