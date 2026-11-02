import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_CONDITION = 4

# Players and their checkers in order
ALL_CHECKERS = ["X", "O", "V", "H", "M"]

# Game settings for submission
NUM_PLAYERS = 2
CHECKERS = ALL_CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print top labels A, B, C, ...
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    sep_line = "+" + "---+" * cols
    for row in board:
        print(sep_line)
        print("| " + " | ".join(row) + " |")
    print(sep_line)


def is_valid_column(col_input, cols):
    if len(col_input) != 1 or not ('A' <= col_input <= chr(ord('A') + cols - 1)):
        return False
    return True


def get_column_index(col_input):
    return ord(col_input) - ord('A')


def place_checker(board, col, checker):
    """
    Place checker in the given column.
    The checker falls to the lowest empty slot.
    Returns True if placed, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[r][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[r+i][c] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Diagonal check (down-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[r+i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Diagonal check (down-left)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, cols):
            count = 0
            for i in range(WIN_CONDITION):
                if board[r+i][c-i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    return False


def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True


def get_player_input(current_checker, cols):
    while True:
        col_input = input(f"Player {current_checker}, please enter a column: ").upper().strip()
        if not is_valid_column(col_input, cols):
            # Invalid input, ask again
            continue
        col_index = get_column_index(col_input)
        return col_index


def main():
    board = create_board(ROWS, COLUMNS)
    cols = COLUMNS
    rows = ROWS
    num_players = NUM_PLAYERS
    checkers = CHECKERS

    current_player_index = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        current_checker = checkers[current_player_index]
        col = get_player_input(current_checker, cols)

        placed = place_checker(board, col, current_checker)
        if not placed:
            # Column full, player loses turn (no repeats)
            # Just skip turn according to spec
            current_player_index = (current_player_index + 1) % num_players
            print_board(board)
            continue

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
