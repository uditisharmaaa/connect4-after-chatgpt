import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win


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

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)]))

    # Print board content
    for r in range(len(board)):
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
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except TypeError:
            print("Invalid input. Please enter a letter (e.g., A, B, C).")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (bool, int) - True if the checker was placed successfully, False otherwise.
               The integer is the row index where the checker was placed, or -1 if full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row up
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r
    return False, -1  # Column is full


def check_win(board, checker, last_row, last_col, win_condition):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.
        win_condition (int): Number of checkers needed in a row to win.

    Returns:
        bool: True if the current player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(max(0, last_col - (win_condition - 1)), min(num_cols, last_col + win_condition)):
        if board[last_row][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(max(0, last_row - (win_condition - 1)), min(num_rows, last_row + win_condition)):
        if board[r][last_col] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start from the top-leftmost possible position of a winning diagonal containing (last_row, last_col)
    start_row_tlbr = max(0, last_row - (win_condition - 1))
    start_col_tlbr = max(0, last_col - (win_condition - 1))
    
    # Adjust start position to ensure it's on the same diagonal
    while start_row_tlbr - start_col_tlbr != last_row - last_col:
        if start_row_tlbr - start_col_tlbr < last_row - last_col:
            start_row_tlbr += 1
        else:
            start_col_tlbr += 1
        # Prevent going out of bounds
        if start_row_tlbr >= num_rows or start_col_tlbr >= num_cols:
            break

    r, c = start_row_tlbr, start_col_tlbr
    while r < num_rows and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check diagonal (bottom-left to top-right)
    count = 0
    # Start from the bottom-leftmost possible position of a winning diagonal containing (last_row, last_col)
    start_row_bltr = min(num_rows - 1, last_row + (win_condition - 1))
    start_col_bltr = max(0, last_col - (win_condition - 1))
    
    # Adjust start position to ensure it's on the same diagonal
    while start_row_bltr + start_col_bltr != last_row + last_col:
        if start_row_bltr + start_col_bltr < last_row + last_col:
            start_row_bltr -= 1
        else:
            start_col_bltr += 1
        # Prevent going out of bounds
        if start_row_bltr < 0 or start_col_bltr >= num_cols:
            break

    r, c = start_row_bltr, start_col_bltr
    while r >= 0 and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

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
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        col_index = get_column_input(current_player_checker, NUM_COLS)
        placed_successfully, last_placed_row = drop_checker(board, col_index, current_player_checker)

        if not placed_successfully:
            print("That column is full! Please choose another column.")
            # Player does not lose turn, continue to next iteration for same player
            continue
        else:
            last_placed_col = col_index

        print_board(board)  # Print board after placing checker

        if check_win(board, current_player_checker, last_placed_row, last_placed_col, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full! It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
