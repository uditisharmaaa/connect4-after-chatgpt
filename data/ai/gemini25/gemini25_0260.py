import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Clears the screen and prints the Connect 4 board.
    """
    os.system('clear')  # Clear the console for a clean display

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board content
    for row_idx in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for col_idx in range(len(board[0])):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

# --- Game Logic Functions ---

def get_player_input(current_player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < board_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + board_cols - 1)}.")
                continue
            return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    return False

def check_win(board, checker, win_condition):
    """
    Checks if the current player has won horizontally, vertically, or diagonally.
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

    # Check ascending diagonal (bottom-left to top-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check descending diagonal (top-left to bottom-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (game is a draw).
    """
    for row in board:
        if " " in row:
            return False
    return True

# --- Main Game Loop ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    players_checkers = CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        current_player_checker = players_checkers[current_player_index]
        print_board(board)

        col_input_valid = False
        while not col_input_valid:
            chosen_col_index = get_player_input(current_player_checker, NUM_COLS)
            if place_checker(board, chosen_col_index, current_player_checker):
                col_input_valid = True
            else:
                print(f"Column {chr(ord('A') + chosen_col_index)} is full. Please choose another column.")

        print_board(board) # Print board after checker is placed

        if check_win(board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            break
        elif check_draw(board):
            print("The board is full. It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
