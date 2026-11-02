import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def get_column_labels(cols):
    """
    Generates alphabetical labels for columns (A, B, C, ...).
    """
    labels = []
    for i in range(cols):
        if i < 26:  # Only A-Z supported
            labels.append(chr(ord('A') + i))
        else:
            # Handle cases beyond Z if needed, though assignment limits to 26
            labels.append(str(i)) # Fallback, not expected for current constraints
    return labels

def print_board(board, col_labels):
    """
    Prints the Connect 4 board with column labels.
    """
    os.system('clear')  # Clear screen for fresh board display

    # Print column labels
    print(" ", end="")
    for label in col_labels:
        print(f" {label} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(len(col_labels)):
        print("---+", end="")
    print()

    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        # Print row separator
        print("+", end="")
        for _ in range(len(col_labels)):
            print("---+", end="")
        print()

# --- Game Logic ---

def get_player_input(player_name, current_player_checker, col_labels):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            if col_char not in col_labels:
                print(f"Invalid column '{col_char}'. Please choose from {', '.join(col_labels)}.")
                continue

            col_index = col_labels.index(col_char)
            return col_index

        except EOFError: # Handles Ctrl+D gracefully
            print("\nGame interrupted. Exiting.")
            sys.exit()
        except KeyboardInterrupt: # Handles Ctrl+C gracefully
            print("\nGame interrupted. Exiting.")
            sys.exit()


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, r, col_index # Return success and position
    return False, -1, -1 # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win (4 in a row).
    Checks horizontally, vertically, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Helper function to count consecutive checkers
    def count_consecutive(r_start, c_start, r_dir, c_dir):
        count = 0
        current_r, current_c = r_start, c_start
        while 0 <= current_r < rows and \
              0 <= current_c < cols and \
              board[current_r][current_c] == checker:
            count += 1
            current_r += r_dir
            current_c += c_dir
        return count

    # Check horizontally
    # Count left from last_col, then right (excluding last_col itself to avoid double counting)
    horiz_count = count_consecutive(last_row, last_col, 0, -1) + count_consecutive(last_row, last_col + 1, 0, 1)
    if horiz_count >= WIN_CONDITION:
        return True

    # Check vertically
    # Count down from last_row (no need to check up, as checkers fall)
    vert_count = count_consecutive(last_row, last_col, 1, 0)
    if vert_count >= WIN_CONDITION:
        return True

    # Check diagonal (top-left to bottom-right)
    # Start from the last_row, last_col and go up-left until out of bounds or different checker,
    # then go down-right from one step right-down of last_row, last_col
    diag1_count = count_consecutive(last_row, last_col, -1, -1) + count_consecutive(last_row + 1, last_col + 1, 1, 1)
    if diag1_count >= WIN_CONDITION:
        return True

    # Check diagonal (top-right to bottom-left)
    # Start from the last_row, last_col and go up-right until out of bounds or different checker,
    # then go down-left from one step left-down of last_row, last_col
    diag2_count = count_consecutive(last_row, last_col, -1, 1) + count_consecutive(last_row + 1, last_col - 1, 1, -1)
    if diag2_count >= WIN_CONDITION:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (draw condition).
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found

def main():
    """
    Main function to run the Connect 4 game.
    """
    # Validate global constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit()
    if not (1 <= NUM_COLS <= 26): # Max 26 for A-Z labels
        print("Error: NUM_COLS must be between 1 and 26.")
        sys.exit()
    if not (WIN_CONDITION <= NUM_ROWS and WIN_CONDITION <= NUM_COLS):
        print("Warning: WIN_CONDITION might be too high for board dimensions.")

    board = create_board(NUM_ROWS, NUM_COLS)
    col_labels = get_column_labels(NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randrange(NUM_PLAYERS)
    print("Welcome to Connect 4!")
    print_board(board, col_labels)
    print(f"Player {players[current_player_index]} goes first!")

    game_over = False
    while not game_over:
        current_player_checker = players[current_player_index]

        col_index = get_player_input(f"Player {current_player_checker}", current_player_checker, col_labels)

        success, last_row, last_col = drop_checker(board, col_index, current_player_checker)

        if not success:
            print(f"Column {col_labels[col_index]} is full. Please choose another column.")
            # Player does not lose turn, stays the same
        else:
            print_board(board, col_labels)

            if check_win(board, current_player_checker, last_row, last_col):
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print("The board is full. It's a draw!")
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("Game Over. Thanks for playing!")

if __name__ == "__main__":
    main()
