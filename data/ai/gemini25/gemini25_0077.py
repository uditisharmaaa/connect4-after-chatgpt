import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
        list: A 2D list representing the board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board with column labels.

    Args:
        board (list): The 2D list representing the current board state.
    """
    clear_screen()
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

def get_player_input(player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < board_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a column between A and {chr(ord('A') + board_cols - 1)}.")
        except Exception:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the current board state.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False

def check_win(board, checker, win_condition):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The 2D list representing the current board state.
        checker (str): The checker symbol of the player to check.
        win_condition (int): Number of consecutive checkers needed to win.

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
    for c in range(cols):
        for r in range(rows - win_condition + 1):
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
        board (list): The 2D list representing the current board state.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Runs the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    player_indices = list(range(NUM_PLAYERS))
    random.shuffle(player_indices)  # Randomly order players
    current_player_index = 0

    game_over = False
    
    while not game_over:
        current_player_checker = CHECKERS[player_indices[current_player_index]]
        print_board(board)

        valid_drop = False
        while not valid_drop:
            col_to_drop = get_player_input(current_player_checker, NUM_COLS)
            if drop_checker(board, col_to_drop, current_player_checker):
                valid_drop = True
            else:
                print(f"Column {chr(ord('A') + col_to_drop)} is full. Please choose another column.")
                # Player does not lose turn for choosing a full column

        # Re-print board after valid move
        print_board(board)

        if check_win(board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\n--- Game Over ---")

if __name__ == "__main__":
    play_game()
