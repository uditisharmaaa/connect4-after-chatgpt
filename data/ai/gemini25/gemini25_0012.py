import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    col_labels = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def get_col_index(col_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding
    0-based integer index.

    Args:
        col_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(col_char) == 1 and 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
        return ord(col_char) - ord('A')
    return -1

def is_valid_column_input(col_input):
    """
    Checks if the user's column input is valid (single uppercase letter
    within the board's column range).

    Args:
        col_input (str): The user's raw input for the column.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    return len(col_input) == 1 and 'A' <= col_input <= string.ascii_uppercase[NUM_COLS - 1]

def get_lowest_empty_row(board, col_index):
    """
    Finds the lowest empty row in a given column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column.

    Returns:
        int: The 0-based index of the lowest empty row, or -1 if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return -1

def drop_checker(board, col_index, player_checker):
    """
    Drops a player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        tuple: (bool, int, int) True if successful, along with the row and column
               where the checker was placed. False and (-1, -1) if the column is full.
    """
    row = get_lowest_empty_row(board, col_index)
    if row != -1:
        board[row][col_index] = player_checker
        return True, row, col_index
    return False, -1, -1

# --- Win Condition Functions ---

def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker at (last_row, last_col).

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        last_row (int): The row where the last checker was placed.
        last_col (int): The column where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    if check_direction(board, player_checker, last_row, last_col, 0, 1): return True
    # Check vertical
    if check_direction(board, player_checker, last_row, last_col, 1, 0): return True
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, player_checker, last_row, last_col, 1, 1): return True
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, player_checker, last_row, last_col, 1, -1): return True
    return False

def check_direction(board, player_checker, r, c, dr, dc):
    """
    Checks for a win in a specific direction from a given cell.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol to look for.
        r (int): Starting row.
        c (int): Starting column.
        dr (int): Row increment for the direction.
        dc (int): Column increment for the direction.

    Returns:
        bool: True if WIN_CONDITION checkers are found in a row in that direction, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    count = 0
    # Check in positive direction
    for i in range(WIN_CONDITION):
        curr_r, curr_c = r + i * dr, c + i * dc
        if 0 <= curr_r < rows and 0 <= curr_c < cols and board[curr_r][curr_c] == player_checker:
            count += 1
        else:
            break
    if count >= WIN_CONDITION:
        return True

    # Reset count and check in negative direction (if dr or dc allows it)
    # This ensures we check *around* the placed checker, not just starting from it
    # E.g., for horizontal, if checker is placed in middle of 4, need to check left and right
    count = 1 # The placed checker itself counts as 1

    # Check 'negative' direction (e.g., left for horizontal, up for vertical, etc.)
    for i in range(1, WIN_CONDITION):
        curr_r, curr_c = r - i * dr, c - i * dc
        if 0 <= curr_r < rows and 0 <= curr_c < cols and board[curr_r][curr_c] == player_checker:
            count += 1
        else:
            break
    
    # Check 'positive' direction (e.g., right for horizontal, down for vertical, etc.)
    for i in range(1, WIN_CONDITION):
        curr_r, curr_c = r + i * dr, c + i * dc
        if 0 <= curr_r < rows and 0 <= curr_c < cols and board[curr_r][curr_c] == player_checker:
            count += 1
        else:
            break

    return count >= WIN_CONDITION


def check_draw(board):
    """
    Checks if the board is completely filled (game is a draw).

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winning_player_checker = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        valid_input = False
        col_char = ""
        col_index = -1

        while not valid_input:
            col_char = input().strip().upper()
            if not is_valid_column_input(col_char):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
                continue

            col_index = get_col_index(col_char)
            if col_index == -1: # Should not happen if is_valid_column_input passes, but good for safety
                print("Invalid column. Please enter a letter corresponding to a valid column.")
                continue
            
            # Check if column is full *before* attempting to drop
            if get_lowest_empty_row(board, col_index) == -1:
                print(f"Column {col_char} is full. Please choose another column.")
            else:
                valid_input = True

        placed_successfully, last_row, last_col = drop_checker(board, col_index, current_player_checker)

        # The 'if not placed_successfully' check below is technically redundant due to the valid_input loop,
        # but kept for robustness and clear separation of concerns.
        if not placed_successfully:
            # This branch should ideally not be reached if validation is perfect.
            print(f"Failed to place checker in column {col_char}. This shouldn't happen after validation.")
            continue # Player effectively loses turn due to unexpected error
        
        # Check for win
        if check_win(board, current_player_checker, last_row, last_col):
            winning_player_checker = current_player_checker
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            game_over = True
        else:
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over - display final board and result
    print_board(board)
    if winning_player_checker:
        print(f"Player {winning_player_checker} won!")
    else:
        print("It's a draw!")

# --- Main Execution ---

if __name__ == "__main__":
    play_game()
