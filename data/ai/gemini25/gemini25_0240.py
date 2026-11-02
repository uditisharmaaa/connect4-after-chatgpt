import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


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
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(num_cols):
        print(f"{string.ascii_uppercase[col_index]}   ", end="")
    print()

    # Print board content
    for row_index in range(num_rows):
        print("+---+", end="")
        for _ in range(num_cols - 1):
            print("---+", end="")
        print("---+")

        print("|", end="")
        for col_index in range(num_cols):
            print(f" {board[row_index][col_index]} |", end="")
        print()

    # Print bottom border
    print("+---+", end="")
    for _ in range(num_cols - 1):
        print("---+", end="")
    print("---+")


def get_player_input(player_checker, board_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol for the current player.
        board_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= string.ascii_uppercase[board_cols - 1]):
                print(f"Invalid input. Please enter a single letter from A to {string.ascii_uppercase[board_cols - 1]}.")
                continue

            col_index = ord(col_char) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please enter a letter corresponding to a column.")


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for row_index in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker):
    """
    Checks if the current player has achieved a win condition.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check for N in a row
    def check_line(r, c, dr, dc):
        count = 0
        for i in range(WIN_CONDITION):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols and board[nr][nc] == player_checker:
                count += 1
            else:
                break
        return count == WIN_CONDITION

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if check_line(r, c, 0, 1):
                return True

    # Check vertical
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols):
            if check_line(r, c, 1, 0):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if check_line(r, c, 1, 1):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, num_cols):
            if check_line(r, c, 1, -1):
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
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)

        col_index = get_player_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_index, current_player_checker):
            if check_win(board, current_player_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = PLAYER_CHECKERS[current_player_index]
        else:
            print("Column is full. Please choose another column.")
            # Player does not lose turn, will be asked again for valid input in next iteration


if __name__ == "__main__":
    main()
