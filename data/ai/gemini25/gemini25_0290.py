import os
import random
import sys

# --- Global Constants ---
# Board dimensions
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)

# Player configuration
NUM_PLAYERS = 2  # Between 2 and 5 players
# Checkers for players. The first NUM_PLAYERS checkers will be used.
CHECKERS = ["X", "O", "V", "H", "M"]

# Win condition
WIN_CONDITION = 4  # Number of checkers in a row to win

# Board cell representation
EMPTY_CELL = " "

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # Use 'cls' for Windows, 'clear' for Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')


def create_board():
    """
    Creates an empty Connect 4 game board initialized with whitespaces.

    Returns:
        list[list[str]]: The game board represented as a 2D list.
    """
    return [[EMPTY_CELL for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """
    Prints the current state of the Connect 4 board to the console.

    Args:
        board (list[list[str]]): The game board.
    """
    clear_screen()

    # Print column labels (A B C ...)
    print("  " + "   ".join(COLUMN_LABELS))

    # Print the board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")  # Top border of the row
        row_content = []
        for c in range(NUM_COLS):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")  # Cells and right border

    print("+---" * NUM_COLS + "+")  # Bottom border of the entire board


def get_player_input(current_player_checker):
    """
    Prompts the current player for their move (column choice) and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

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

            # Check if the input is a single letter and within valid range
            if len(user_input) != 1 or not 'A' <= user_input <= COLUMN_LABELS[-1]:
                print(f"Error: Invalid column. Please enter a letter from A to {COLUMN_LABELS[-1]}.")
                continue

            # Convert column letter to 0-indexed column number
            col_index = ord(user_input) - ord('A')
            return col_index

        except EOFError:
            print("\nGame terminated by user.")
            sys.exit() # Exit cleanly if EOF (e.g., Ctrl+D) is encountered
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the lowest available space in the specified column.

    Args:
        board (list[list[str]]): The game board.
        col_index (int): The 0-indexed column number where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple[bool, int, int]: A tuple containing:
            - bool: True if the checker was successfully dropped, False otherwise (column full).
            - int: The row index where the checker was placed (or -1 if failed).
            - int: The column index where the checker was placed (or -1 if failed).
    """
    if not (0 <= col_index < NUM_COLS):
        # This case should ideally be caught by input validation, but good for robustness
        return False, -1, -1

    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = player_checker
            return True, r, col_index
    return False, -1, -1  # Column is full


def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list[list[str]]): The game board.
        player_checker (str): The checker symbol of the current player.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Define directions for checking: (row_delta, col_delta)
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal (down-right)
        (1, -1)   # Diagonal (down-left)
    ]

    for dr, dc in directions:
        count = 1  # Count of consecutive checkers, starting with the last placed one

        # Check in positive direction
        for i in range(1, WIN_CONDITION):
            r, c = last_row + dr * i, last_col + dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                break
        if count >= WIN_CONDITION:
            return True

        # Check in negative direction (reset count and check from last placed checker again)
        # Note: We already counted the `last_placed` checker once.
        # If we go left for horizontal, we need to ensure not to double count
        # the center `last_placed` checker. A simpler way is to check the entire line
        # by checking both directions from `last_placed` and adding 1 for `last_placed` itself.

        # Re-initialize count to 1 (for the current checker itself)
        count = 1
        # Check in one direction (e.g., right for horizontal, down for vertical, etc.)
        for i in range(1, WIN_CONDITION):
            r, c = last_row + dr * i, last_col + dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                break

        # Check in the opposite direction (e.g., left for horizontal, up for vertical, etc.)
        for i in range(1, WIN_CONDITION):
            r, c = last_row - dr * i, last_col - dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                break

        if count >= WIN_CONDITION:
            return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list[list[str]]): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == EMPTY_CELL:
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw


def main():
    """
    Main function to run the Connect 4 game.
    """
    # --- Initialization ---
    game_board = create_board()
    player_checkers_in_play = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randrange(NUM_PLAYERS)  # Randomly choose first player
    game_over = False
    winning_player_checker = None

    print_board(game_board)
    print(f"Player {player_checkers_in_play[current_player_index]} starts!")

    # --- Game Phase ---
    while not game_over:
        current_player_checker = player_checkers_in_play[current_player_index]

        col_index = get_player_input(current_player_checker)

        # Attempt to drop the checker
        placed_successfully, last_row, last_col = drop_checker(game_board, col_index, current_player_checker)

        if not placed_successfully:
            print(f"Error: Column {COLUMN_LABELS[col_index]} is full. Please choose another column.")
            # Player does not lose turn, will be asked again
            continue

        print_board(game_board)

        # Check for win condition
        if check_win(game_board, current_player_checker, last_row, last_col):
            winning_player_checker = current_player_checker
            game_over = True
            break  # Exit game loop

        # Check for draw condition
        if check_draw(game_board):
            game_over = True
            break  # Exit game loop

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # --- Game End ---
    print("\n--- Game Over ---")
    if winning_player_checker:
        print(f"Player {winning_player_checker} won!")
    else:
        print("It's a draw!")
    print_board(game_board) # Print final board one last time


if __name__ == "__main__":
    main()
