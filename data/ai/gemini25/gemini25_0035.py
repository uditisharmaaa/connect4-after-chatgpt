import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
# Ensure enough checkers for the number of players
if NUM_PLAYERS > len(PLAYER_CHECKERS):
    raise ValueError(f"Not enough checkers defined for {NUM_PLAYERS} players.")

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
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its integer index.

    Args:
        column_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based index of the column, or None if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1 or not column_char.isalpha():
        return None
    
    col_index = ord(column_char.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return None

def is_valid_move(board, col_index):
    """
    Checks if a move to a specific column is valid.

    Args:
        board (list): The 2D list representing the board.
        col_index (int): The 0-based index of the column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    if not (0 <= col_index < num_cols):
        return False  # Column index out of bounds

    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        tuple or None: A tuple (row, col) of where the checker landed,
                       or None if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return (r, col_index)
    return None  # Column is full

def check_win(board, last_row, last_col, checker, win_condition):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The 2D list representing the board.
        last_row (int): The row of the last placed checker.
        last_col (int): The column of the last placed checker.
        checker (str): The symbol of the checker that was just placed.
        win_condition (int): The number of checkers needed to win.

    Returns:
        bool: True if a win is detected, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[last_row][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(num_rows):
        if board[r][last_col] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    # Start at the point that allows for a full diagonal check
    # Iterate through potential starting points of a winning line
    for r_start in range(num_rows - win_condition + 1):
        for c_start in range(num_cols - win_condition + 1):
            count = 0
            for i in range(win_condition):
                if board[r_start + i][c_start + i] == checker:
                    count += 1
                else:
                    break # Break if sequence is broken
            if count >= win_condition:
                return True

    # Check negative diagonal (top-left to bottom-right)
    # Start at the point that allows for a full diagonal check
    # Iterate through potential starting points of a winning line
    for r_start in range(num_rows - win_condition + 1):
        for c_start in range(win_condition - 1, num_cols):
            count = 0
            for i in range(win_condition):
                if board[r_start + i][c_start - i] == checker:
                    count += 1
                else:
                    break # Break if sequence is broken
            if count >= win_condition:
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, resulting in a draw.

    Args:
        board (list): The 2D list representing the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_game():
    """
    Manages the Connect 4 game flow.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner = None

    while not game_over:
        current_checker = players[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_input = False
        col_index = -1
        while not valid_input:
            user_input = input().strip().upper()
            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., 'A'):")
                continue

            col_index = get_column_index(user_input, NUM_COLS)

            if col_index is None:
                print("Invalid column. Please enter a letter within the board range:")
            elif not is_valid_move(board, col_index):
                print("Column is full or invalid. Please choose another column:")
            else:
                valid_input = True

        # Player made a valid move
        last_pos = drop_checker(board, col_index, current_checker)

        # Check for win
        if last_pos and check_win(board, last_pos[0], last_pos[1], current_checker, WIN_CONDITION):
            winner = current_checker
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board) # Print final board
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Start the game ---
if __name__ == "__main__":
    play_game()
