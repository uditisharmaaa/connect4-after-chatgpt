import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (max 5 players as per assignment)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def get_column_label(col_index):
    """
    Converts a column index (0-based) to its corresponding uppercase letter.
    Supports up to 26 columns (A-Z).
    """
    if 0 <= col_index < 26:
        return chr(ord('A') + col_index)
    return ""


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    """
    clear_screen()

    # Print column labels
    print("  ", end="")
    for col in range(len(board[0])):
        print(f"{get_column_label(col)}   ", end="")
    print()

    # Print board rows
    for row in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for col in range(len(board[0])):
            print(f" {board[row][col]} |", end="")
        print()
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


def clear_screen():
    """
    Clears the console screen. Works for Linux/Unix terminals.
    """
    os.system('clear')


def get_column_from_input(user_input, num_cols):
    """
    Converts a user-entered column letter (e.g., 'A') to a 0-based index.
    Returns -1 for invalid input.
    """
    if not isinstance(user_input, str) or len(user_input) != 1:
        return -1
    col_char = user_input.upper()
    col_index = ord(col_char) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return -1


def place_checker(board, col_index, checker):
    """
    Places a checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):  # Iterate from bottom to top
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


# --- Game Logic Functions ---
def check_win(board, checker, win_condition):
    """
    Checks if the given checker has formed a win_condition in a row
    (horizontally, vertically, or diagonally).
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for r in range(rows - win_condition + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - win_condition + 1):
        for c in range(win_condition - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full (no more empty spaces).
    """
    for row in board:
        if " " in row:
            return False
    return True


def get_valid_player_input(board, current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Repeats until a valid, non-full column is chosen.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").strip()
            col_index = get_column_from_input(player_input, num_cols)

            if col_index == -1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A).")
                continue

            # Check if the column is full
            if board[0][col_index] != " ":  # Check the top-most row
                print(f"Column {get_column_label(col_index)} is full. Please choose another column.")
                continue

            return col_index
        except EOFError:
            print("\nExiting game due to EOF. Goodbye!")
            sys.exit()
        except KeyboardInterrupt:
            print("\nExiting game. Goodbye!")
            sys.exit()


# --- Main Game Loop ---
def main():
    """
    Main function to run the Connect 4 game.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26.")
        return
    if not (1 <= NUM_ROWS):
        print("Error: NUM_ROWS must be at least 1.")
        return
    if not (1 <= WIN_CONDITION):
        print("Error: WIN_CONDITION must be at least 1.")
        return

    # Initialize game
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    print("Welcome to Connect 4!")
    print(f"Playing with {NUM_PLAYERS} players: {', '.join(players)}")
    print(f"Board size: {NUM_ROWS} rows x {NUM_COLS} columns")
    print(f"Win condition: {WIN_CONDITION} in a row")
    input("Press Enter to start...")

    # Game phase
    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)

        col_to_place = get_valid_player_input(board, current_player_checker, NUM_COLS)

        # Place the checker
        place_checker(board, col_to_place, current_player_checker)

        # Check for win
        if check_win(board, current_player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
