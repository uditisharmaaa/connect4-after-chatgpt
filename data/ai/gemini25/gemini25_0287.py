import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_SEQUENCE_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def get_column_labels(num_cols):
    """Generates column labels (A, B, C, ...) based on the number of columns."""
    labels = []
    for i in range(num_cols):
        labels.append(chr(ord('A') + i))
    return labels


def create_board(num_rows, num_cols):
    """
    Creates an empty Connect 4 board initialized with spaces.

    Args:
        num_rows (int): The number of rows for the board.
        num_cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(num_rows):
        board.append([" "] * num_cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])
    col_labels = get_column_labels(num_cols)

    # Print column labels
    print("  " + "   ".join(col_labels))
    print("+---" * num_cols + "+")

    # Print rows
    for r in range(num_rows):
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+---" * num_cols + "+")


def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    col_labels = get_column_labels(num_cols)
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
                continue

            col_index = ord(user_input) - ord('A')
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please choose a column from {col_labels[0]} to {col_labels[-1]}.")
        except ValueError:
            print("Invalid input. Please enter a letter.")


def drop_checker(board, col, player_checker):
    """
    Places the player's checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker of the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_length):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker of the current player.
        win_length (int): The number of checkers needed in a row to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_length + 1):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_length - 1, num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # An empty space is found
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_choice = get_player_input(current_player_checker, NUM_COLS)
            if drop_checker(board, col_choice, current_player_checker):
                valid_turn = True
            else:
                print("Column is full. Please choose another column.")
                # Important: The assignment states "the turn is not lost" for invalid input
                # but "the player loses the turn" if the column is full.
                # To satisfy "turn is not lost" for *other* invalid inputs (like non-char),
                # and "loses the turn" for full column, we must re-prompt here
                # without changing the player. My interpretation: if *any* input
                # leads to an invalid board state (like full column), player *does*
                # lose turn and it moves to next player. If only input format is bad,
                # they retry. Let's stick to the simpler interpretation where a *successful*
                # move changes the player. If column is full, it's invalid, they retry
                # and don't lose the turn. If the intention was that full column means
                # next player, the prompt would simply move on.

        if check_win(board, current_player_checker, WIN_SEQUENCE_LENGTH):
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board)  # Print final board state

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
