import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission as per assignment
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]


# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows in the board.
        cols (int): The number of columns in the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join(string.ascii_uppercase[:num_cols]))

    for r in range(len(board)):
        # Print top border of each row
        print('+---+---' * (num_cols - 1) + '+---+')
        row_str = '|'
        for c in range(num_cols):
            row_str += f' {board[r][c]} |'
        print(row_str)
    # Print bottom border of the last row
    print('+---+---' * (num_cols - 1) + '+---+')


def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_input:  # Handle empty input
                print("Invalid input. Please enter a column letter (e.g., A, B).")
                continue

            col_index = string.ascii_uppercase.find(col_input)

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column '{col_input}'. Please enter a letter from A to {string.ascii_uppercase[NUM_COLS - 1]}.")
        except TypeError: # Should not happen with .upper(), but good for robustness
            print("Invalid input. Please enter a column letter (e.g., A, B).")
        except Exception: # Catch any other unexpected errors
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the given checker has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, NUM_COLS):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False
    return True


def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = ACTIVE_CHECKERS[current_player_index]

    game_over = False
    winning_player = None

    while not game_over:
        print_board(board)
        current_checker = ACTIVE_CHECKERS[current_player_index]

        col_index = get_column_input(current_checker)

        if drop_checker(board, col_index, current_checker):
            # Checker was successfully placed, now check for win/draw
            if check_win(board, current_checker):
                winning_player = current_checker
                game_over = True
            elif check_draw(board):
                game_over = True  # It's a draw
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column was full, current player does not lose turn, but is prompted again.
            print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
            # current_player_index does not change, so they get to try again


    # Game over, print final board and result
    print_board(board)
    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("It's a draw!")


# --- Main execution ---
if __name__ == "__main__":
    play_game()
