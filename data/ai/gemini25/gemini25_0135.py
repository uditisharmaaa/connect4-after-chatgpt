import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Clears the screen and prints the current state of the board.
    """
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

# --- Game Logic ---

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its integer index.
    Returns -1 if the character is invalid.
    """
    if len(column_char) != 1 or not column_char.isalpha():
        return -1
    index = ord(column_char.upper()) - ord('A')
    if 0 <= index < num_cols:
        return index
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a column index is valid and if the column is not full.
    """
    if not (0 <= col_index < len(board[0])):
        return False
    return board[0][col_index] == EMPTY_CELL

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the lowest available spot in the specified column.
    Returns the row index where the checker was placed.
    Assumes the move is valid.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = checker
            return r
    return -1 # Should not happen if is_valid_move is checked

def check_win(board, row, col, checker, win_condition):
    """
    Checks if the last placed checker resulted in a win (horizontal, vertical, or diagonal).
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers
    def count_consecutive(delta_row, delta_col):
        count = 0
        for i in range(-win_condition + 1, win_condition):
            r, c = row + i * delta_row, col + i * delta_col
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
                if count >= win_condition:
                    return True
            else:
                count = 0
        return False

    # Check horizontal
    if count_consecutive(0, 1):
        return True
    # Check vertical
    if count_consecutive(1, 0):
        return True
    # Check main diagonal (top-left to bottom-right)
    if count_consecutive(1, 1):
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if count_consecutive(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

def get_player_input(board, current_player_char, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Repeats until a valid input is provided.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_char}, please enter a column: ").strip().upper()
            col_index = get_column_index(player_input, num_cols)

            if col_index == -1:
                print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")
            elif not is_valid_move(board, col_index):
                print("Column is full or out of bounds. Please choose another column.")
            else:
                return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {CHECKERS[current_player_index]} goes first!")

    while not game_over:
        current_player_char = CHECKERS[current_player_index]
        num_cols = len(board[0])

        col_index = get_player_input(board, current_player_char, num_cols)
        row_placed = drop_checker(board, col_index, current_player_char)

        print_board(board)

        # Check for win
        if check_win(board, row_placed, col_index, current_player_char, WIN_CONDITION):
            winner_checker = current_player_char
            game_over = True
        # Check for draw
        elif check_draw(board):
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
