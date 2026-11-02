import os
import random
import sys

# Constants for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLUMNS = 7
NUM_PLAYERS = 2

# Max 26 columns supported
assert BOARD_COLUMNS <= 26, "Maximum 26 columns supported."
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."

# Checkers assigned in order, max 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    # Creates a BOARD_ROWS x BOARD_COLUMNS board filled with spaces
    return [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers as letters A..G (or up to the number of columns)
    col_labels = [chr(ord('A') + i) for i in range(BOARD_COLUMNS)]
    print("  " + "   ".join(col_labels))

    # Print each row with separators and cells
    sep_line = "+" + ("---+" * BOARD_COLUMNS)
    for r in range(BOARD_ROWS):
        print(sep_line)
        row_cells = "| " + " | ".join(board[r]) + " |"
        print(row_cells)
    print(sep_line)

def column_letter_to_index(letter):
    letter = letter.upper()
    if len(letter) != 1:
        return None
    idx = ord(letter) - ord('A')
    if 0 <= idx < BOARD_COLUMNS:
        return idx
    return None

def is_column_full(board, col_idx):
    # If top cell (row 0) is not empty, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    """
    Place checker in the lowest available spot in the given column.
    Return True if placed, False if column full.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    """
    Check horizontally, vertically, and diagonally if there are
    4 checkers in a row belonging to player with 'checker'.
    """

    # Horizontal check
    for r in range(BOARD_ROWS):
        count = 0
        for c in range(BOARD_COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(BOARD_COLUMNS):
        count = 0
        for r in range(BOARD_ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Diagonal checks
    # Down-right (\) diagonals
    # Start from every cell that could have 4 in a row diagonally
    for r in range(BOARD_ROWS - 3):
        for c in range(BOARD_COLUMNS - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True

    # Down-left (/) diagonals
    for r in range(BOARD_ROWS - 3):
        for c in range(3, BOARD_COLUMNS):
            if (board[r][c] == checker and
                board[r+1][c-1] == checker and
                board[r+2][c-2] == checker and
                board[r+3][c-3] == checker):
                return True

    return False

def board_full(board):
    # Board is full if no spaces remain in top row columns (means no moves left)
    for c in range(BOARD_COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def input_column(current_player):
    # Prompt until valid column letter is input (A - corresponding board columns)
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or not ('A' <= user_input <= chr(ord('A') + BOARD_COLUMNS - 1)):
            # Invalid input
            continue
        col_idx = column_letter_to_index(user_input)
        if col_idx is None:
            continue
        return col_idx

def main():
    board = create_board()
    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_idx]

        col_idx = input_column(current_checker)

        if is_column_full(board, col_idx):
            # According to prompt: if column is full, turn is invalid and player loses the turn
            # so no placement, just advance turn.
            # But first print board so user can see no change
            print_board(board)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        placed = place_checker(board, col_idx, current_checker)
        assert placed, "Should have placed because we checked column not full."

        print_board(board)

        # Check for a win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for a draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
