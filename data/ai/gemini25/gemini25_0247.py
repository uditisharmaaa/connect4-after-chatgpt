import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers needed to win

# Valid checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_EMPTY_CELL = " "


# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with empty cells.
    """
    return [[BOARD_EMPTY_CELL for _ in range(cols)] for _ in range(rows)]


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
    print("  ", end="")
    for i in range(num_cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print the board content
    for r in range(num_rows):
        print("+---" * num_cols + "+")
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * num_cols + "+")


def get_player_input(player_name, current_player_checker, num_cols):
    """
    Prompts the current player for their move and validates the input.

    Args:
        player_name (str): The name/identifier of the current player.
        current_player_checker (str): The checker symbol for the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., A, B).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if not ('A' <= col_char <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single column letter (e.g., A, B).")


def drop_checker(board, col_index, checker):
    """
    Places the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol of the current player.

    Returns:
        tuple: (True, row_index) if the checker was successfully placed,
               (False, None) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == BOARD_EMPTY_CELL:
            board[r][col_index] = checker
            return True, r  # Return True and the row where it was placed
    return False, None  # Column is full


def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player who just moved.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(max(0, last_col - WIN_CONDITION + 1), min(num_cols, last_col + WIN_CONDITION)):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(max(0, last_row - WIN_CONDITION + 1), min(num_rows, last_row + WIN_CONDITION)):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start checking from WIN_CONDITION-1 positions up and left from last_row, last_col
    start_row = max(0, last_row - WIN_CONDITION + 1)
    start_col = max(0, last_col - WIN_CONDITION + 1)
    for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
        r, c = last_row + i, last_col + i
        if 0 <= r < num_rows and 0 <= c < num_cols:
            if board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0

    # Check diagonal (top-right to bottom-left)
    count = 0
    # Start checking from WIN_CONDITION-1 positions up and right from last_row, last_col
    for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
        r, c = last_row + i, last_col - i
        if 0 <= r < num_rows and 0 <= c < num_cols:
            if board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == BOARD_EMPTY_CELL:
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw


# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers based on NUM_PLAYERS
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winning_player_checker = None

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        
        # Get valid input from the current player
        col_index = get_player_input(f"Player {current_player_checker}", current_player_checker, NUM_COLS)

        # Attempt to drop the checker
        successfully_dropped, last_row = drop_checker(board, col_index, current_player_checker)

        if not successfully_dropped:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn if column is full
            continue 
        
        # Check for win condition
        if check_win(board, current_player_checker, last_row, col_index):
            winning_player_checker = current_player_checker
            game_over = True
            print_board(board) # Print final board
            print(f"Player {winning_player_checker} won!")
            break

        # Check for draw condition
        if check_draw(board):
            game_over = True
            print_board(board) # Print final board
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("Game over!")


if __name__ == "__main__":
    main()
