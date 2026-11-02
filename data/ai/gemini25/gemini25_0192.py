import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def get_column_letter(col_index):
    """Converts a column index (0-based) to its corresponding uppercase letter."""
    return chr(ord('A') + col_index)


def get_column_index(col_letter):
    """Converts an uppercase column letter to its corresponding 0-based index."""
    return ord(col_letter) - ord('A')


def create_board(rows, cols):
    """
    Creates and initializes a new Connect 4 game board.
    The board is a list of lists, filled with whitespace characters.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col in range(NUM_COLS):
        print(f" {get_column_letter(col)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers and horizontal separators
    for row in range(NUM_ROWS):
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
        print()

        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()


def is_valid_column_input(col_input):
    """
    Checks if the user's column input is a single uppercase letter
    within the valid range of columns.
    """
    if len(col_input) != 1:
        return False
    col_input = col_input.upper()
    if not 'A' <= col_input <= get_column_letter(NUM_COLS - 1):
        return False
    return True


def get_player_move(player_name, board):
    """
    Prompts the current player for a column choice and validates the input.
    Continues prompting until a valid and available column is chosen.
    Returns the 0-based index of the chosen column.
    """
    while True:
        try:
            col_input = input(f"Player {player_name}, please enter a column: ").upper()

            if not is_valid_column_input(col_input):
                print(f"Invalid input. Please enter a single letter between A and {get_column_letter(NUM_COLS - 1)}.")
                continue

            col_index = get_column_index(col_input)

            # Check if the column is full
            if board[0][col_index] != " ":  # Check the top row of the chosen column
                print(f"Column {col_input} is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print(f"Invalid input. Please enter a single letter between A and {get_column_letter(NUM_COLS - 1)}.")
        except IndexError:
            # This should ideally not happen if is_valid_column_input is robust
            print("An unexpected error occurred with column selection. Please try again.")


def place_checker(board, col_index, checker):
    """
    Places the given checker in the lowest available space of the specified column.
    Returns the (row, col) coordinates where the checker was placed, or None if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None  # Column is full


def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker results in a win (4 in a row)
    horizontally, vertically, or diagonally.
    """
    # Helper function to count consecutive checkers in a direction
    def count_consecutive(delta_row, delta_col):
        count = 0
        # Check in one direction
        r, c = last_row, last_col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col

        # Check in the opposite direction (excluding the starting checker again)
        r, c = last_row - delta_row, last_col - delta_col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= delta_row
            c -= delta_col
        return count

    # Check horizontal win
    if count_consecutive(0, 1) >= WIN_SEQUENCE_LENGTH:
        return True

    # Check vertical win
    if count_consecutive(1, 0) >= WIN_SEQUENCE_LENGTH:
        return True

    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1) >= WIN_SEQUENCE_LENGTH:
        return True

    # Check anti-diagonal (top-right to bottom-left)
    if count_consecutive(1, -1) >= WIN_SEQUENCE_LENGTH:
        return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full


def main():
    """
    Main function to run the Connect 4 game.
    """
    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = players[current_player_index]

    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {current_checker} starts first!")

    while not game_over:
        current_checker = players[current_player_index]

        col_index = get_player_move(current_checker, board)
        placement = place_checker(board, col_index, current_checker)

        # If placement is None, it means the column was full,
        # but our get_player_move should prevent this.
        # This acts as a safeguard.
        if placement is None:
            print("Error: Column was full after all. This should not happen.")
            continue

        last_row, last_col = placement
        print_board(board)

        if check_win(board, current_checker, last_row, last_col):
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # --- Game End ---
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

    print("Thanks for playing Connect 4!")


if __name__ == "__main__":
    main()
