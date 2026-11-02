import os
import random
import string

# --- Constants (Global Variables) ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players (X, O, V, H, M)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Function Definitions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def print_board(board):
    """
    Prints the Connect 4 board with column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))

    # Print board rows
    for r in range(num_rows):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

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
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
                print(f"Invalid input. Please enter a single letter from A to {string.ascii_uppercase[num_cols - 1]}.")
                continue
            
            col_index = ord(col_char) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (True, row_placed) if the checker was placed successfully,
               (False, None) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r  # Return True and the row where it was placed
    return False, None  # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a line
    def check_line(r_start, c_start, r_dir, c_dir):
        count = 0
        for i in range(4):
            r, c = r_start + i * r_dir, c_start + i * c_dir
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
            else:
                break
        return count == 4

    # --- Check Horizontal ---
    for c in range(max(0, last_col - 3), min(num_cols - 3, last_col + 1)):
        if check_line(last_row, c, 0, 1):
            return True

    # --- Check Vertical ---
    for r in range(max(0, last_row - 3), min(num_rows - 3, last_row + 1)):
        if check_line(r, last_col, 1, 0):
            return True

    # --- Check Diagonal (Top-Left to Bottom-Right) ---
    for r_offset in range(-3, 1):
        if check_line(last_row + r_offset, last_col + r_offset, 1, 1):
            return True

    # --- Check Diagonal (Bottom-Left to Top-Right) ---
    for r_offset in range(-3, 1):
        if check_line(last_row - r_offset, last_col + r_offset, -1, 1):
            return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (a draw).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = len(CHECKERS)

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)
        
        col_index = get_column_input(current_player_checker, NUM_COLS)

        placed, last_row = drop_checker(board, col_index, current_player_checker)

        if not placed:
            print("Column is full! Please choose another column. You lose your turn.")
            # The assignment states "the turn is not lost" for invalid input,
            # but for a full column, it says "the turn is invalid and the player loses the turn."
            # We'll implement it as per the "loses the turn" part for a full column.
            # No need to change current_player_index as it explicitly says turn is lost.
        else:
            # Check for win
            if check_win(board, current_player_checker, last_row, col_index):
                print_board(board)
                winner_checker = current_player_checker
                game_over = True
            # Check for draw
            elif check_draw(board):
                print_board(board)
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % num_players

    # Game over message
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
