import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers needed to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# Valid column letters for input
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(NUM_COLS)]


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    The board is a list of lists.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear' if os.name == 'posix' else 'cls')


def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels (A, B, C, ...) and a grid format.
    """
    clear_screen()

    # Print column labels
    col_labels = ' '.join([f" {letter}" for letter in COLUMN_LETTERS])
    print(f" {col_labels}")

    # Print top border
    print(f"+{'+---' * NUM_COLS}+")

    # Print rows
    for r in range(NUM_ROWS):
        row_content = '|'.join([f" {board[r][c]} " for c in range(NUM_COLS)])
        print(f"|{row_content}|")
        print(f"+{'+---' * NUM_COLS}+")


def get_player_move(player_checker):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) > 1:
                print("Invalid input. Please enter a single column letter (e.g., A).")
                continue

            col_char = user_input[0]

            if col_char not in COLUMN_LETTERS:
                print(f"Invalid column '{col_char}'. Please choose from {', '.join(COLUMN_LETTERS)}.")
                continue

            col = ord(col_char) - ord('A')
            return col
        except Exception:
            print("An unexpected error occurred during input. Please try again.")


def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col] == ' ':
            board[r][col] = player_checker
            return True, r, col  # Return success and the position
    return False, -1, -1  # Column is full


def check_win(board, row, col, player_checker):
    """
    Checks if the last placed checker at (row, col) results in a win.
    Checks horizontally, vertically, and both diagonals.
    """

    # Helper function to count consecutive checkers in a direction
    def count_consecutive(delta_row, delta_col):
        count = 0
        # Check forward direction
        r, c = row, col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
            count += 1
            r += delta_row
            c += delta_col
        # Check backward direction (don't double count the original checker)
        r, c = row - delta_row, col - delta_col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
            count += 1
            r -= delta_row
            c -= delta_col
        return count

    # Check horizontal win
    if count_consecutive(0, 1) >= WIN_CONDITION:
        return True

    # Check vertical win
    if count_consecutive(1, 0) >= WIN_CONDITION:
        return True

    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1) >= WIN_CONDITION:
        return True

    # Check diagonal (top-right to bottom-left)
    if count_consecutive(1, -1) >= WIN_CONDITION:
        return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # An empty space is found, not a draw
    return True  # Board is full


def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_COLS > 26:
        print("Error: Maximum 26 columns supported for letter labels.")
        sys.exit(1)

    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)

    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    game_board = create_board(NUM_ROWS, NUM_COLS)
    game_over = False
    winner = None

    print_board(game_board)

    while not game_over:
        player_checker = players[current_player_idx]
        print(f"It's Player {player_checker}'s turn.")

        col_choice = get_player_move(player_checker)

        # Validate if the chosen column is within bounds (already done by get_player_move, but good practice)
        if not (0 <= col_choice < NUM_COLS):
            print("Invalid column selection. Please try again.")
            continue # Player does not lose turn

        success, last_row, last_col = drop_checker(game_board, col_choice, player_checker)

        if not success:
            print(f"Column {COLUMN_LETTERS[col_choice]} is full. Please choose another column.")
            continue  # Player does not lose turn

        print_board(game_board)

        if check_win(game_board, last_row, last_col, player_checker):
            winner = player_checker
            game_over = True
        elif check_draw(game_board):
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
