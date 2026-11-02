import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Creates an empty game board initialized with whitespaces."""
    return [[" "] * cols for _ in range(rows)]


def print_board(board):
    """Prints the Connect 4 board with column labels."""
    clear_screen()
    cols = len(board[0])
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:cols]))
    for r in range(len(board)):
        print("+---" * cols + "+")
        print("| " + " | ".join(board[r]) + " |")
    print("+---" * cols + "+")


def get_column_input(player_checker, num_cols):
    """
    Prompts the player for column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        col_char = input(f"Player {player_checker}, please enter a column: ").upper()
        if len(col_char) == 1 and 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
            return ord(col_char) - ord('A')
        else:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")


def drop_checker(board, col_idx, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = player_checker
            return True
    return False


def check_win(board, player_checker, win_count):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_count + 1):
            if all(board[r][c + i] == player_checker for i in range(win_count)):
                return True

    # Check vertical
    for r in range(rows - win_count + 1):
        for c in range(cols):
            if all(board[r + i][c] == player_checker for i in range(win_count)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_count + 1):
        for c in range(cols - win_count + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_count)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_count - 1, rows):
        for c in range(cols - win_count + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_count)):
                return True

    return False


def check_draw(board):
    """Checks if the board is full, indicating a draw."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full


# --- Main Game Logic ---
def play_game():
    """Manages the Connect 4 game flow."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        player_checker = CHECKERS[current_player_idx]
        print_board(board)

        while True:
            col_idx = get_column_input(player_checker, NUM_COLS)
            if drop_checker(board, col_idx, player_checker):
                break  # Checker dropped successfully, break inner loop
            else:
                print("Column is full. Please choose another column.")
                # Player does not lose turn, re-prompt for input

        # After every turn, print the updated board
        print_board(board)

        if check_win(board, player_checker, WIN_CONDITION):
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            print("The board is full. It's a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
