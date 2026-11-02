import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

# Players configuration for 2 players as per submission requirements
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])

    # Print column headers (A-G)
    headers = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(headers))

    # Print board with separators
    for r in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * cols)


def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    col_num = ord(col_char) - ord('A')
    return 0 <= col_num < cols


def get_column_index(col_char):
    return ord(col_char) - ord('A')


def place_checker(board, col, checker):
    """
    Places checker into column `col` if possible.
    Returns True if placed, False if column is full.
    """
    # place at the lowest free row from bottom to top
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # column full


def board_full(board):
    # If any cell on top row is empty, board is not full
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + offset][c] == checker for offset in range(WIN_LENGTH)):
                return True

    # Diagonal check (down-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + offset][c + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Diagonal check (down-left)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r + offset][c - offset] == checker for offset in range(WIN_LENGTH)):
                return True

    return False


def input_column(current_player, board):
    cols = len(board[0])
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col = get_column_index(user_input)
        # Check if column is full
        if board[0][col] != " ":
            # Column is full - player loses turn (according to spec)
            print(f"Column {user_input} is full. You lose your turn.")
            return None
        return col


def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYERS
    num_players = len(players)

    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]

        col = input_column(current_checker, board)
        if col is not None:
            placed = place_checker(board, col, current_checker)
            # We already checked for full column, but double check in case
            if not placed:
                # According to spec, losing turn handled above, so just continue gameplay
                pass

            print_board(board)

            # Win check
            if placed and check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Draw check
            if board_full(board):
                print("Game is a draw.")
                break

        # Move to next player (even if player lost turn)
        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
