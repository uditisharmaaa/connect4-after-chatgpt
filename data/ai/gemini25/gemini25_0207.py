import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---

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
        list: A 2D list representing the board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    cols = len(board[0])
    rows = len(board)

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(cols):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print the board with separators
    for r in range(rows):
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(cols):
            print(f" {board[r][c]} |", end="")
        print()
    # Print the last horizontal separator
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()


def get_column_input(current_player_checker):
    """
    Prompts the current player for column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    cols = NUM_COLS
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).upper()

            if not user_input:
                print("Input cannot be empty. Please try again.")
                continue

            # Check if input is a single letter
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < cols:
                return col_index
            else:
                print(f"Column '{col_char}' is out of bounds. Valid columns are A-{chr(ord('A') + cols - 1)}.")
        except ValueError:
            print("Invalid input. Please enter a letter corresponding to a column.")


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: (True, row_index) if the checker was successfully dropped,
               (False, None) if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, r  # Return row index where checker was placed
    return False, None  # Column is full


def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker at (last_row, last_col).

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    win_len = WIN_CONDITION

    # Helper function to check a direction
    def check_direction(dr, dc):
        count = 1  # Start with the placed checker itself
        # Check in one direction
        for i in range(1, win_len):
            r, c = last_row + dr * i, last_col + dc * i
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
                count += 1
            else:
                break
        # Check in the opposite direction
        for i in range(1, win_len):
            r, c = last_row - dr * i, last_col - dc * i
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
                count += 1
            else:
                break
        return count >= win_len

    # Check horizontal
    if check_direction(0, 1):
        return True
    # Check vertical
    if check_direction(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True
    # Check diagonal (top-right to bottom-left)
    if check_direction(1, -1):
        return True

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False  # An empty space is found, not a draw
    return True  # No empty spaces, it's a draw


# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}'s turn.")

        col_index = get_column_input(current_player_checker)
        checker_placed, last_row = drop_checker(board, col_index, current_player_checker)

        if not checker_placed:
            print(f"Column {chr(ord('A') + col_index)} is full. You lose this turn. Please try another column next time.")
            # Player effectively loses their turn, but we don't want to switch to the next player.
            # Instead, the game loop continues, and it will re-ask the current player for input.
            # However, the assignment states "the turn is invalid and the player loses the turn."
            # This implies the player should not get to try again in the same turn.
            # To adhere to the prompt's implied behavior (player losing turn and next player plays),
            # we will advance to the next player.
            # If the interpretation was to simply re-prompt until a valid drop, the 'continue' would suffice.
            # Based on "the turn is invalid and the player loses the turn" -> switch player.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Move to the next player's turn directly.

        # Check for win
        if check_win(board, current_player_checker, last_row, col_index):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
