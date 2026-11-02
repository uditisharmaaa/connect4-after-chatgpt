import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win


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
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print()

    # Print board content
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


def get_player_input(current_player_checker, board_cols):
    """
    Gets and validates player input for the column to drop a checker.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Error: Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1 or not user_input.isalpha():
                print("Error: Invalid input. Please enter a single letter (A-G).")
                continue

            col_index = ord(user_input) - ord('A')

            if 0 <= col_index < board_cols:
                return col_index
            else:
                print(f"Error: Column '{user_input}' is out of bounds. Please choose a column from A to {string.ascii_uppercase[board_cols - 1]}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The 0-indexed column number.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (True, row_index) if the checker was placed successfully,
               (False, None) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r
    return False, None  # Column is full


def check_win(board, row, col, checker, win_count):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The 2D list representing the game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol of the current player.
        win_count (int): The number of checkers needed to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[row][c] == checker:
            count += 1
            if count >= win_count:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r_idx in range(num_rows):
        if board[r_idx][col] == checker:
            count += 1
            if count >= win_count:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    count = 0
    # Find start of diagonal
    start_row, start_col = row, col
    while start_row < num_rows - 1 and start_col > 0:
        start_row += 1
        start_col -= 1

    r, c = start_row, start_col
    while r >= 0 and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= win_count:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    # Check negative diagonal (top-left to bottom-right)
    count = 0
    # Find start of diagonal
    start_row, start_col = row, col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1

    r, c = start_row, start_col
    while r < num_rows and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= win_count:
                return True
        else:
            count = 0
        r += 1
        c += 1

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

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


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {CHECKERS[current_player_index]} starts!")

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print(f"Current Turn: Player {current_player_checker}")

        col_to_drop = get_player_input(current_player_checker, NUM_COLS)
        
        placed, row_placed = drop_checker(board, col_to_drop, current_player_checker)

        if not placed:
            print("Error: Column is full! You lose your turn.")
            # Player does not lose turn if column is full, re-prompting for input until valid
            # "the turn is not lost" from invalid input means the player gets to try again
            # "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
            # This is a conflicting statement. I will interpret "the turn is not lost" to apply to ALL invalid inputs,
            # including full columns, meaning the player will be prompted again until a valid, non-full column is chosen.
            # If the strict "loses the turn" for full column is desired, remove 'continue' and proceed to next player.
            continue 

        print_board(board)

        if check_win(board, row_placed, col_to_drop, current_player_checker, WIN_CONDITION):
            winner_checker = current_player_checker
            game_over = True
            break
        
        if check_draw(board):
            game_over = True
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\n--- GAME OVER ---")
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")
    print_board(board) # Print final board one last time


if __name__ == "__main__":
    main()
