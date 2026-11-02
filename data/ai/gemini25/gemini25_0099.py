import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- HELPER FUNCTIONS ---
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
        list[list[str]]: A 2D list representing the game board,
                         initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list[list[str]]): The game board to print.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * num_cols + "+")


def get_column_input(current_player_checker, num_cols):
    """
    Gets and validates a column input from the current player.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            prompt_message = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt_message).upper()

            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., A).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column '{user_input}'. Please enter a letter from A to {chr(ord('A') + num_cols - 1)}.")
        except IndexError:
            print("Invalid input. Please enter a column letter (e.g., A).")
        except ValueError:
            print("Invalid input. Please enter a column letter (e.g., A).")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list[list[str]]): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol to place.

    Returns:
        tuple[bool, int, int]: A tuple indicating if the drop was successful (bool),
                               the row index where the checker landed (int), and
                               the column index (int).
                               Returns (False, -1, -1) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r, col_index
    return False, -1, -1  # Column is full


def check_win(board, r_last, c_last, checker):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list[list[str]]): The game board.
        r_last (int): The row index of the last placed checker.
        c_last (int): The column index of the last placed checker.
        checker (str): The checker symbol of the player who just moved.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[r_last][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(num_rows):
        if board[r][c_last] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start from the top-leftmost cell of the current diagonal
    start_row = r_last - min(r_last, c_last)
    start_col = c_last - min(r_last, c_last)
    while start_row < num_rows and start_col < num_cols:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    # Check diagonal (bottom-left to top-right)
    count = 0
    # Start from the bottom-leftmost cell of the current diagonal
    start_row = r_last + min(num_rows - 1 - r_last, c_last)
    start_col = c_last - min(num_rows - 1 - r_last, c_last)
    while start_row >= 0 and start_col < num_cols:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list[list[str]]): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = len(CHECKERS)

    player_turn = random.randrange(num_players)  # Randomly select first player
    game_over = False
    last_placed_row, last_placed_col = -1, -1  # To store the last move for win checking

    while not game_over:
        current_player_checker = CHECKERS[player_turn]
        print_board(board)

        valid_move = False
        while not valid_move:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            success, r, c = drop_checker(board, col_index, current_player_checker)

            if success:
                valid_move = True
                last_placed_row, last_placed_col = r, c
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # Player does not lose turn for a full column

        print_board(board)  # Print board after a valid move

        if check_win(board, last_placed_row, last_placed_col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            player_turn = (player_turn + 1) % num_players


if __name__ == "__main__":
    main()
