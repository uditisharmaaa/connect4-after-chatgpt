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
    cols = len(board[0])
    rows = len(board)

    # Print column labels (A, B, C...)
    print("  " + "   ".join(string.ascii_uppercase[:cols]))
    for r in range(rows):
        print("+---" * cols + "+")
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * cols + "+")


def is_valid_column_input(col_input, max_cols):
    """
    Validates if the user's column input is valid.

    Args:
        col_input (str): The user's input for the column.
        max_cols (int): The maximum number of columns allowed.

    Returns:
        int or None: The 0-indexed column number if valid, None otherwise.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return None
    
    col_input = col_input.upper()
    if 'A' <= col_input <= string.ascii_uppercase[max_cols - 1]:
        return ord(col_input) - ord('A')
    return None


def get_next_available_row(board, col):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to check.

    Returns:
        int or None: The row index if a spot is available, None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to place the checker.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    row = get_next_available_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False


def check_win(board, checker, win_condition):
    """
    Checks if a player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for r in range(rows - win_condition + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
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
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty spot exists, not a draw
    return True  # No empty spots, it's a draw


# --- Main Game Logic ---
def play_game():
    """
    Runs the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False
    
    while not game_over:
        print_board(board)
        current_checker = PLAYER_CHECKERS[current_player_index]
        
        col_choice = None
        valid_move_made = False

        while not valid_move_made:
            prompt = f"Player {current_checker}, please enter a column: "
            user_input = input(prompt).strip()
            
            col_index = is_valid_column_input(user_input, NUM_COLS)
            
            if col_index is None:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
            elif not (0 <= col_index < NUM_COLS):
                print(f"Column {user_input.upper()} is out of bounds. Please choose a column from A to {string.ascii_uppercase[NUM_COLS-1]}.")
            elif not place_checker(board, col_index, current_checker):
                print(f"Column {user_input.upper()} is full. Please choose another column.")
            else:
                valid_move_made = True
        
        # Check for win
        if check_win(board, current_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
