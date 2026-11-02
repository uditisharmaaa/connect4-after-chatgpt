import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Board Functions ---
def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the screen

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print board content
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")


# --- Game Logic Functions ---
def get_column_input(player_checker, num_cols):
    """Prompts the player for a column input and validates it."""
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + num_cols - 1)):
                raise ValueError
            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B).")


def place_checker(board, col, checker):
    """Places a checker in the specified column. Returns True if successful, False otherwise."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """Checks if the given checker has won the game."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """Checks if the board is completely filled (a draw)."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)

        col_index = get_column_input(current_checker, NUM_COLS)

        if place_checker(board, col_index, current_checker):
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player's turn is not lost, they re-enter input in the next loop iteration


if __name__ == "__main__":
    main()
