import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# Game settings (for submission)
NUM_PLAYERS = 2


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    columns = len(board[0])
    # Column headers: letters starting from 'A'
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(columns))
    separator = "+" + "---+" * columns
    print(header)
    print(separator)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(separator)


def is_valid_column_input(user_input, columns):
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col_index = ord(user_input.upper()) - ord('A')
    if col_index < 0 or col_index >= columns:
        return False
    return True


def get_lowest_empty_row(board, col_index):
    # From bottom to top, find the first empty row in column
    for row_index in reversed(range(len(board))):
        if board[row_index][col_index] == " ":
            return row_index
    return None  # Column full


def place_checker(board, col_index, checker):
    row_index = get_lowest_empty_row(board, col_index)
    if row_index is None:
        return False
    board[row_index][col_index] = checker
    return True


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontally
    for row in range(rows):
        count = 0
        for col in range(cols):
            count = count + 1 if board[row][col] == checker else 0
            if count >= WIN_COUNT:
                return True

    # Check vertically
    for col in range(cols):
        count = 0
        for row in range(rows):
            count = count + 1 if board[row][col] == checker else 0
            if count >= WIN_COUNT:
                return True

    # Check diagonally (top-left to bottom-right)
    for row in range(rows - WIN_COUNT + 1):
        for col in range(cols - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonally (bottom-left to top-right)
    for row in range(WIN_COUNT - 1, rows):
        for col in range(cols - WIN_COUNT + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_COUNT)):
                return True

    return False


def check_draw(board):
    # If any cell in the top row is empty, game is not draw
    return all(cell != " " for cell in board[0])


def main():
    # Select players' checkers accordingly
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return
    players = CHECKERS[:NUM_PLAYERS]

    board = create_board(ROWS, COLUMNS)
    # Randomly select the first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        user_input = input().strip().upper()

        # Validate input
        if not is_valid_column_input(user_input, COLUMNS):
            # Invalid input -> ask again, turn not lost
            continue

        col_index = ord(user_input) - ord('A')

        # Try to place checker; if column full, player loses turn
        if not place_checker(board, col_index, current_checker):
            # Column full: player loses turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
