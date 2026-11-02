import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables (initialized later) ---
board = []
player_checkers = []


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board of the specified dimensions.
    Each cell is initialized with a whitespace.
    """
    new_board = []
    for _ in range(rows):
        new_board.append([" "] * cols)
    return new_board


def print_board(current_board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels (A, B, C, ...) and row separators.
    """
    os.system('clear')  # Clear the screen before printing

    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print board content
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {current_board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")


def get_column_from_input(prompt):
    """
    Prompts the user for a column input and validates it.
    Returns the 0-indexed column number if valid, otherwise None.
    """
    while True:
        user_input = input(prompt).strip().upper()

        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")
            continue

        col_char_index = ord(user_input) - ord('A')
        if 0 <= col_char_index < NUM_COLS:
            return col_char_index
        else:
            print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[NUM_COLS - 1]}.")


def drop_checker(current_board, col, checker):
    """
    Places a checker in the specified column.
    Returns the row where the checker was placed if successful,
    otherwise returns -1 if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if current_board[r][col] == " ":
            current_board[r][col] = checker
            return r
    return -1  # Column is full


def check_win(current_board, checker, last_row, last_col):
    """
    Checks if the given checker has formed a Connect 4 win
    after being placed at (last_row, last_col).
    Checks horizontally, vertically, and diagonally.
    """
    # Helper function to count consecutive checkers in a direction
    def count_consecutive(row, col, dr, dc):
        count = 0
        while 0 <= row < NUM_ROWS and \
              0 <= col < NUM_COLS and \
              current_board[row][col] == checker:
            count += 1
            row += dr
            col += dc
        return count

    # Check horizontal win
    count_left = count_consecutive(last_row, last_col - 1, 0, -1)
    count_right = count_consecutive(last_row, last_col + 1, 0, 1)
    if count_left + 1 + count_right >= 4:
        return True

    # Check vertical win
    count_up = count_consecutive(last_row - 1, last_col, -1, 0)
    count_down = count_consecutive(last_row + 1, last_col, 1, 0)
    if count_up + 1 + count_down >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count_up_left = count_consecutive(last_row - 1, last_col - 1, -1, -1)
    count_down_right = count_consecutive(last_row + 1, last_col + 1, 1, 1)
    if count_up_left + 1 + count_down_right >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count_up_right = count_consecutive(last_row - 1, last_col + 1, -1, 1)
    count_down_left = count_consecutive(last_row + 1, last_col - 1, 1, -1)
    if count_up_right + 1 + count_down_left >= 4:
        return True

    return False


def check_draw(current_board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if current_board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found


def play_game():
    """
    Main function to run the Connect 4 game.
    """
    global board, player_checkers

    # Initialize game settings
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = player_checkers[current_player_index]

    print_board(board)
    print(f"Player {current_checker} starts first!")

    game_over = False
    while not game_over:
        print(f"Player {current_checker}, please enter a column:")

        chosen_col_index = get_column_from_input(f"Player {current_checker}'s turn: ")

        if chosen_col_index is None: # Should not happen with current get_column_from_input, but good for safety
            continue

        placed_row = drop_checker(board, chosen_col_index, current_checker)

        if placed_row == -1:
            print(f"Column {string.ascii_uppercase[chosen_col_index]} is full. Please choose another column.")
            # Player does not lose turn, re-prompt for input
            continue

        print_board(board)

        # Check for win
        if check_win(board, current_checker, placed_row, chosen_col_index):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = player_checkers[current_player_index]


# --- Start the game ---
if __name__ == "__main__":
    play_game()
