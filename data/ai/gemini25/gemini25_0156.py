import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables (initialized later) ---
board = []
current_player_index = 0
players = []

# --- Functions ---

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

    # Print column labels (A, B, C, ...)
    col_labels = [string.ascii_uppercase[i] for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    for r in range(num_rows):
        # Print horizontal separator
        print("+---" * num_cols + "+")
        # Print row content
        row_content = []
        for c in range(num_cols):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")
    # Print bottom separator
    print("+---" * num_cols + "+")

def get_player_input(player_checker, board):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    valid_cols = [string.ascii_uppercase[i] for i in range(num_cols)]

    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            if not col_input:
                print("Invalid input. Please enter a column letter (e.g., A).")
                continue

            if col_input not in valid_cols:
                print(f"Invalid column '{col_input}'. Please choose a column from {', '.join(valid_cols)}.")
                continue

            col_index = ord(col_input) - ord('A')

            if is_column_full(board, col_index):
                print(f"Column {col_input} is full. Please choose another column.")
                continue

            return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single uppercase letter for the column.")

def is_column_full(board, col_index):
    """
    Checks if a given column is completely filled with checkers.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number to check.

    Returns:
        bool: True if the column is full, False otherwise.
    """
    return board[0][col_index] != ' '

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number to drop the checker into.
        checker (str): The checker symbol of the player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
        int: The row index where the checker was placed, or -1 if placement failed.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True, r
    return False, -1 # Column was full, though this should be prevented by prior validation

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player who just moved.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a direction
    def count_consecutive(row, col, dr, dc):
        count = 0
        r, c = row, col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Check horizontal
    count = count_consecutive(last_row, last_col, 0, 1) + count_consecutive(last_row, last_col, 0, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check vertical
    count = count_consecutive(last_row, last_col, 1, 0) + count_consecutive(last_row, last_col, -1, 0) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonal (top-left to bottom-right)
    count = count_consecutive(last_row, last_col, 1, 1) + count_consecutive(last_row, last_col, -1, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonal (top-right to bottom-left)
    count = count_consecutive(last_row, last_col, 1, -1) + count_consecutive(last_row, last_col, -1, 1) - 1
    if count >= WIN_CONDITION:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, resulting in a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

def setup_game():
    """
    Initializes game parameters, including players and the starting player.
    """
    global board, players, current_player_index

    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

def game_loop():
    """
    Manages the main game flow, turns, input, and win/draw conditions.
    """
    global current_player_index

    setup_game()
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = players[current_player_index]
        print_board(board)

        col_index = get_player_input(current_checker, board)
        
        # Drop checker and get the actual row where it landed
        placed, last_row = drop_checker(board, col_index, current_checker)
        last_col = col_index # This is the column where it was dropped

        if placed:
            if check_win(board, current_checker, last_row, last_col):
                winner_checker = current_checker
                game_over = True
            elif check_draw(board):
                game_over = True # No winner, but board is full
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # If 'placed' is False, it means the column was full, but get_player_input
        # already handles this, so 'placed' should always be True here if input is valid.

    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

# --- Main execution ---
if __name__ == "__main__":
    game_loop()
