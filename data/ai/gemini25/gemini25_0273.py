import os
import random
import string

# --- Global Constants (Adjust these for testing different setups) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Max 5 players
WIN_LENGTH = 4

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
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print()

    # Print the board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

def get_column_input(current_player_checker, num_cols):
    """
    Gets and validates column input from the player.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            col_input = input(prompt).strip().upper()

            if not col_input.isalpha() or len(col_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_input) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
        except TypeError:
            print("Invalid input. Please enter a letter.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker, win_length):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        win_length (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_length + 1):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_length + 1):
        for c in range(cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_length - 1, rows):
        for c in range(cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full (a draw).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces, it's a draw

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_index, current_player_checker):
            # Checker was successfully dropped
            if check_win(board, current_player_checker, WIN_LENGTH):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
            # Player does not lose turn if column is full, try again. (Based on assignment interpretation)


if __name__ == "__main__":
    main()
