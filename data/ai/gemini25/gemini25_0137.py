import os
import random
import string

# --- Constants (Global Variables) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Can be 2, 3, 4, or 5
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]


# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels (A, B, C, ...) and grid lines.
    """
    clear_screen()  # Clear screen before printing
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(user_input) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and "
                      f"{string.ascii_uppercase[num_cols - 1]}.")
        except ValueError:
            print("Invalid input. Please enter a letter.")


def place_checker(board, col, checker):
    """
    Places the checker in the lowest available spot in the given column.
    Returns True if successful, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r  # Return True and the row where it was placed
    return False, -1  # Column is full


def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker.
    Checks horizontally, vertically, and both diagonals.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers
    def count_consecutive(delta_row, delta_col):
        count = 0
        # Check in one direction
        r, c = last_row, last_col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        # Check in the opposite direction (excluding the starting checker again)
        r, c = last_row - delta_row, last_col - delta_col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r -= delta_row
            c -= delta_col
        return count

    # 1. Check Horizontal Win
    if count_consecutive(0, 1) >= WIN_CONDITION:
        return True

    # 2. Check Vertical Win
    if count_consecutive(1, 0) >= WIN_CONDITION:
        return True

    # 3. Check Diagonal Win (top-left to bottom-right)
    if count_consecutive(1, 1) >= WIN_CONDITION:
        return True

    # 4. Check Diagonal Win (top-right to bottom-left)
    if count_consecutive(1, -1) >= WIN_CONDITION:
        return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found


# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]  # Select checkers based on NUM_PLAYERS
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"The first player is {players[current_player_index]}!")

    while not game_over:
        current_player_checker = players[current_player_index]

        # Get and validate player input
        valid_move = False
        placed_row = -1
        placed_col = -1
        while not valid_move:
            chosen_col_index = get_player_input(current_player_checker, NUM_COLS)
            success, r_placed = place_checker(board, chosen_col_index, current_player_checker)

            if success:
                valid_move = True
                placed_row = r_placed
                placed_col = chosen_col_index
            else:
                print(f"Column {string.ascii_uppercase[chosen_col_index]} is full. Please choose another column.")

        # Print the updated board
        print_board(board)

        # Check for win condition
        if check_win(board, current_player_checker, placed_row, placed_col):
            winner_checker = current_player_checker
            game_over = True
            print(f"Player {winner_checker} won!")
        # Check for draw condition
        elif check_draw(board):
            game_over = True
            print("It's a draw!")
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# --- Entry Point ---
if __name__ == "__main__":
    play_game()
