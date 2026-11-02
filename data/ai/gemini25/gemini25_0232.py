import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = CHECKERS[:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with empty cells.
    """
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)])
    print(header)

    # Print top border
    print("+---" * num_cols + "+")

    # Print rows
    for r in range(len(board)):
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+---" * num_cols + "+")

def get_column_index(col_char, num_cols):
    """
    Converts a column letter (e.g., 'A') to its corresponding 0-based index.

    Args:
        col_char (str): The column letter entered by the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index if valid, otherwise None.
    """
    col_char = col_char.upper()
    if 'A' <= col_char <= chr(ord('A') + num_cols - 1):
        return ord(col_char) - ord('A')
    return None

def is_valid_column_input(col_input, num_cols):
    """
    Checks if the user's column input is valid.

    Args:
        col_input (str): The raw input from the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        bool: True if the input is a single uppercase letter within the valid range, False otherwise.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return False
    
    col_char = col_input.upper()
    return 'A' <= col_char <= chr(ord('A') + num_cols - 1)

def get_player_move(player_checker, board):
    """
    Prompts the current player for a column choice and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-based index of the chosen and validated column.
    """
    num_cols = len(board[0])
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip()

        if not is_valid_column_input(col_input, num_cols):
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")
            continue

        col_index = get_column_index(col_input, num_cols)

        if board[0][col_index] != EMPTY_CELL:  # Check if the top of the column is full
            print("That column is full. Please choose another column.")
            continue
        
        return col_index

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = player_checker
            return True
    return False # Should not happen if `get_player_move` is called first

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (positive slope: /)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (negative slope: \)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
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
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY_CELL:
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False

    while not game_over:
        player_checker = PLAYERS[current_player_index]
        print_board(board)

        col_index = get_player_move(player_checker, board)
        
        # Place the checker
        drop_checker(board, col_index, player_checker)
        
        print_board(board) # Print board after placing checker

        # Check for win
        if check_win(board, player_checker, WIN_CONDITION):
            print(f"Player {player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
