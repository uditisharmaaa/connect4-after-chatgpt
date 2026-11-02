import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

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
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column headers (A, B, C, ...)
    print('  ', end='')
    for i in range(num_cols):
        print(f'{chr(ord("A") + i)}   ', end='')
    print()

    # Print top border
    print('+---' * num_cols + '+')

    # Print board rows
    for r in range(num_rows):
        print('|', end='')
        for c in range(num_cols):
            print(f' {board[r][c]} |', end='')
        print()
        print('+---' * num_cols + '+')

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column '{col_char}'. Please enter a letter from A to {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column number.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        tuple: (bool, int) - True if the checker was placed successfully,
               False otherwise. The row index where the checker landed,
               or -1 if placement failed.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True, r
    return False, -1  # Column is full

def check_win(board, row, col, checker):
    """
    Checks if the last placed checker resulted in a win (4 in a row).

    Args:
        board (list): The game board.
        row (int): The row where the last checker was placed.
        col (int): The column where the last checker was placed.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if a win is detected, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(max(0, col - 3), min(num_cols, col + 4)):
        if board[row][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r_check in range(max(0, row - 3), min(num_rows, row + 4)):
        if board[r_check][col] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find start of diagonal (up-left from current)
    start_row_tl = row
    start_col_tl = col
    while start_row_tl > 0 and start_col_tl > 0 and (row - start_row_tl) < 3 and (col - start_col_tl) < 3:
        start_row_tl -= 1
        start_col_tl -= 1

    for i in range(7):  # Check up to 7 positions along diagonal
        r_check = start_row_tl + i
        c_check = start_col_tl + i
        if 0 <= r_check < num_rows and 0 <= c_check < num_cols:
            if board[r_check][c_check] == checker:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        else:
            count = 0


    # Check diagonal (top-right to bottom-left)
    count = 0
    # Find start of diagonal (up-right from current)
    start_row_tr = row
    start_col_tr = col
    while start_row_tr > 0 and start_col_tr < num_cols - 1 and (row - start_row_tr) < 3 and (start_col_tr - col) < 3:
        start_row_tr -= 1
        start_col_tr += 1

    for i in range(7): # Check up to 7 positions along diagonal
        r_check = start_row_tr + i
        c_check = start_col_tr - i
        if 0 <= r_check < num_rows and 0 <= c_check < num_cols:
            if board[r_check][c_check] == checker:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        else:
            count = 0

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

def play_game():
    """Main function to run the Connect 4 game."""
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26 (for A-Z labels).")
        sys.exit(1)

    players_checkers = CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = players_checkers[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        col_index = get_column_input(current_player_checker, NUM_COLS)

        placed_successfully, row_landed = drop_checker(board, col_index, current_player_checker)

        if not placed_successfully:
            print("Column is full. Please choose another column.")
            # Player does not lose turn, will be prompted again for the same player
            continue
        else:
            # Check for a win
            if check_win(board, row_landed, col_index, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The board is full. It's a draw!")
                game_over = True
            else:
                # Switch to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = players_checkers[current_player_index]

if __name__ == "__main__":
    play_game()
