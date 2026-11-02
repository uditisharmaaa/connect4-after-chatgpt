import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * len(board[0]))


def is_valid_column(col_char):
    return col_char in COLUMN_LABELS


def col_char_to_index(col_char):
    return ord(col_char) - ord('A')


def place_checker(board, col_idx, checker):
    """
    Places checker on the lowest available row in column col_idx.
    Returns True if placed successfully, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # column full


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal down-right
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal up-right
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False


def board_full(board):
    return all(board[0][c] != " " for c in range(len(board[0])))


def get_valid_input(current_checker):
    """
    Prompt user until a valid column letter is entered.
    Validation: uppercase letter, within board columns.
    """
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            # must be single char
            continue
        if not user_input.isalpha():
            continue
        if not is_valid_column(user_input):
            continue
        return user_input


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randrange(NUM_PLAYERS)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]

        col_char = get_valid_input(current_checker)
        col_idx = col_char_to_index(col_char)

        placed = place_checker(board, col_idx, current_checker)
        if not placed:
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check win
        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
