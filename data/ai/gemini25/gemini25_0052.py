import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for A-Z column labels
NUM_PLAYERS = 2  # Between 2 and 5 players

CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win


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
    print("  " + "   ".join(chr(ord('A') + i) for i in range(num_cols)))
    print("+" + "---+" * num_cols)

    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * num_cols)


def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the chosen valid column.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Column '{col_char}' is out of board range. Please choose a column between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("An unexpected error occurred with your input. Please try again.")


def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for row in range(num_rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
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
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check positive diagonal wins (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check negative diagonal wins (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker, NUM_COLS)

        if place_checker(board, col_index, current_player_checker):
            # Check for win
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            # Check for draw
            elif check_draw(board):
                print_board(board)
                print("The board is full! It's a draw!")
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Column is full. Please choose another column.")
            # Player does not lose turn if column is full, they just pick again


if __name__ == "__main__":
    main()
