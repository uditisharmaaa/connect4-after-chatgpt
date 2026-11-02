import os
import random
import string

# --- Global Constants (for easy configuration) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
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
        list: A 2D list representing the game board,
              initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear screen before printing
    rows = len(board)
    cols = len(board[0])

    # Print column labels (A, B, C, ...)
    col_labels = string.ascii_uppercase[:cols]
    print("  " + "   ".join(col_labels))

    # Print top border
    print("+" + "---+".join([""] * cols))

    # Print rows with checkers and separators
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+".join([""] * cols))


def get_column_index(col_char, cols):
    """
    Converts a column character (e.g., 'A') to its integer index.

    Args:
        col_char (str): The uppercase character representing the column.
        cols (int): The total number of columns.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return -1
    col_char = col_char.upper()
    if 'A' <= col_char <= string.ascii_uppercase[cols - 1]:
        return ord(col_char) - ord('A')
    return -1


def is_valid_move(board, col_index):
    """
    Checks if a chosen column is valid for placing a checker.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the chosen column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    if not (0 <= col_index < cols):
        return False  # Column index out of bounds

    # Check if the top-most row in the column is empty
    return board[0][col_index] == " "


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        int: The row index where the checker landed, or -1 if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r  # Return the row where the checker was placed
    return -1  # Column is full (should be caught by is_valid_move)


def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal wins
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c in range(cols):
        for r in range(rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check diagonal (positive slope) wins
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal (negative slope) wins
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
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
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full


# --- Main Game Logic ---
def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            col_index = get_column_index(user_input, NUM_COLS)

            if col_index == -1:
                print("Invalid column. Please enter a letter from A to "
                      f"{string.ascii_uppercase[NUM_COLS - 1]}.")
            elif not is_valid_move(board, col_index):
                print(f"Column {user_input} is full. Please choose another column.")
            else:
                break # Valid input received

        drop_checker(board, col_index, current_checker)

        if check_win(board, current_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over! Thanks for playing.")


if __name__ == "__main__":
    play_game()
