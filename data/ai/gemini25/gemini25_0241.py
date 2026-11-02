import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print()

    # Print board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

def get_col_label(col_index):
    """Converts a column index to its letter label."""
    return string.ascii_uppercase[col_index]

def get_col_index(col_label):
    """Converts a column letter label to its index."""
    return string.ascii_uppercase.index(col_label)

# --- Game Logic Functions ---

def is_valid_column_input(col_input, num_cols):
    """Checks if the user's column input is valid."""
    if not isinstance(col_input, str) or len(col_input) != 1:
        return False
    col_input = col_input.upper()
    if col_input not in string.ascii_uppercase[:num_cols]:
        return False
    return True

def get_next_available_row(board, col_index):
    """Finds the lowest available row in a given column.
    Returns -1 if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return -1 # Column is full

def place_checker(board, col_index, player_checker):
    """Places a checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    row = get_next_available_row(board, col_index)
    if row != -1:
        board[row][col_index] = player_checker
        return True
    return False

def check_win(board, player_checker, win_condition):
    """Checks if the current player has won the game."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check positively sloped diagonals
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check negatively sloped diagonals
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full, indicating a draw."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # There's still an empty space
    return True  # Board is full

# --- Main Game Loop ---

def play_game():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            player_input = input().strip()

            if not is_valid_column_input(player_input, NUM_COLS):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
                continue

            col_index = get_col_index(player_input)

            if get_next_available_row(board, col_index) == -1:
                print(f"Column {get_col_label(col_index)} is full. Please choose another column.")
            else:
                place_checker(board, col_index, current_player_checker)
                valid_turn = True

        if check_win(board, current_player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---

if __name__ == "__main__":
    play_game()
