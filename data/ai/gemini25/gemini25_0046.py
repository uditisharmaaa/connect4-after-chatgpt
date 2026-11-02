import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(' ', end='')
    for col_idx in range(len(board[0])):
        print(f"  {chr(ord('A') + col_idx)} ", end='')
    print()

    # Print top border
    print('+---' * len(board[0]) + '+')

    # Print rows
    for row in board:
        print('|', end='')
        for cell in row:
            print(f" {cell} |", end='')
        print()
        print('+---' * len(board[0]) + '+')

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A') to its 0-based index.
    """
    return ord(column_char.upper()) - ord('A')

def is_valid_column_input(column_char, num_cols):
    """
    Checks if the given column character is a valid input.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return False
    col_idx = get_column_index(column_char)
    return 0 <= col_idx < num_cols

def is_column_full(board, col_idx):
    """
    Checks if a given column is completely filled with checkers.
    """
    return board[0][col_idx] != ' '

def drop_checker(board, col_idx, checker):
    """
    Drops a checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    if is_column_full(board, col_idx):
        return False

    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False # Should not be reached if is_column_full check is done first

# --- Win Condition Functions ---

def check_win(board, checker):
    """
    Checks if the given checker has formed a winning sequence (horizontal, vertical, or diagonal).
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, rows):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True
    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for col_idx in range(len(board[0])):
        if board[0][col_idx] == ' ':  # If any cell in the top row is empty, game is not a draw
            return False
    return True

# --- Main Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    current_checker = PLAYER_CHECKERS[current_player_idx]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_input = False
        while not valid_input:
            column_input = input().strip().upper()

            if not is_valid_column_input(column_input, NUM_COLS):
                print("Invalid input. Please enter a single letter (e.g., A, B, C) within the board limits.")
                continue

            col_idx = get_column_index(column_input)

            if is_column_full(board, col_idx):
                print(f"Column {column_input} is full. Please choose another column.")
                continue

            valid_input = True

        # Drop the checker
        drop_successful = drop_checker(board, col_idx, current_checker)

        # This check should theoretically always be True after the validation loop,
        # but it's good practice for robustness.
        if not drop_successful:
            print(f"An unexpected error occurred dropping checker in column {column_input}. Please try again.")
            continue

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        current_checker = PLAYER_CHECKERS[current_player_idx]

    print("\nGame Over.")

if __name__ == "__main__":
    main()
