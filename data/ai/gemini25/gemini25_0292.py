import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_column_letter(col_index):
    """Converts a column index (0-based) to its corresponding uppercase letter."""
    return chr(ord('A') + col_index)

def get_column_index(col_letter):
    """Converts an uppercase column letter to its corresponding index (0-based)."""
    return ord(col_letter) - ord('A')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the board, initialized with whitespaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for col in range(num_cols):
        print(f" {get_column_letter(col)} ", end="")
    print()

    # Print the board content
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def is_valid_input(player_input, num_cols):
    """
    Validates the player's column input.

    Args:
        player_input (str): The raw input from the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not isinstance(player_input, str) or len(player_input) != 1:
        return False
    
    col_letter = player_input.upper()
    if not 'A' <= col_letter <= get_column_letter(num_cols - 1):
        return False
    
    return True

def get_player_move(current_player_char, num_cols):
    """
    Prompts the current player for their move and validates it.

    Args:
        current_player_char (str): The character representing the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_char}, please enter a column: ").upper()
            if not is_valid_input(player_input, num_cols):
                print(f"Invalid input. Please enter a single letter from A to {get_column_letter(num_cols - 1)}.")
                continue

            col_index = get_column_index(player_input)
            return col_index
        except ValueError:
            print(f"Invalid input. Please enter a single letter from A to {get_column_letter(num_cols - 1)}.")

def drop_checker(board, col_index, player_char):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop into.
        player_char (str): The character of the player making the move.

    Returns:
        int: The row index where the checker was placed, or -1 if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == ' ':
            board[r][col_index] = player_char
            return r
    return -1  # Column is full

def check_win(board, player_char, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        player_char (str): The character of the player to check for a win.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[last_row][c] == player_char:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(num_rows):
        if board[r][last_col] == player_char:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    count = 0
    # Start point for checking (row, col)
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)
    
    r, c = start_row, start_col
    while r < num_rows and c < num_cols:
        if board[r][c] == player_char:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check negative diagonal (top-left to bottom-right)
    count = 0
    # Start point for checking (row, col)
    start_row = last_row - min(last_row, num_cols - 1 - last_col)
    start_col = last_col + min(last_row, num_cols - 1 - last_col)

    r, c = start_row, start_col
    while r < num_rows and c >= 0:
        if board[r][c] == player_char:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c -= 1

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == ' ':
                return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_COLS > 26:
        print("Error: NUM_COLS cannot exceed 26 (due to letter labels).")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    while not game_over:
        current_player_char = players[current_player_index]
        
        col_index = get_player_move(current_player_char, NUM_COLS)

        # Attempt to drop the checker
        row_placed = drop_checker(board, col_index, current_player_char)

        if row_placed == -1:
            clear_screen()
            print_board(board)
            print(f"Column {get_column_letter(col_index)} is full! Player {current_player_char} loses their turn.")
            # Do not change player, they effectively lost a turn by making an invalid move
            continue
        else:
            last_placed_row = row_placed
            last_placed_col = col_index
        
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_player_char, last_placed_row, last_placed_col):
            print(f"Player {current_player_char} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
