import os
import random

# Constants for the game setup
ROWS = 6
COLS = 7
WIN_STREAK = 4
NUM_PLAYERS = 2  # Between 2 and 5
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    # Board is a list of rows; each row is a list of cols
    # Initialize with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers: letters A ... (A+cols-1)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    line = "+" + "---+" * len(board[0])

    for row in range(len(board)):
        print(line)
        row_cells = "|"
        for col in range(len(board[0])):
            row_cells += " {} |".format(board[row][col])
        print(row_cells)
    print(line)


def valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    col = ord(user_input) - ord('A')
    return 0 <= col < cols


def has_space_in_column(board, col):
    return board[0][col] == " "


def place_checker(board, col, checker):
    # Place checker in the lowest empty row in column col
    # Return True if placed, False if no space (should not be called if no space)
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]):
        if board[row][col] == checker:
            count += 1
            if count == WIN_STREAK:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        if check_direction(board, r, 0, 0, 1, checker):
            return True

    # Check vertical
    for c in range(cols):
        if check_direction(board, 0, c, 1, 0, checker):
            return True

    # Check diagonal down-right
    # We check diagonals starting on top row and leftmost column
    for r in range(rows):
        if check_direction(board, r, 0, 1, 1, checker):
            return True
    for c in range(cols):
        if check_direction(board, 0, c, 1, 1, checker):
            return True

    # Check diagonal down-left
    for r in range(rows):
        if check_direction(board, r, cols - 1, 1, -1, checker):
            return True
    for c in range(cols):
        if check_direction(board, 0, c, 1, -1, checker):
            return True

    return False


def is_board_full(board):
    for c in range(len(board[0])):
        if has_space_in_column(board, c):
            return False
    return True


def get_player_input(player_checker, cols):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not valid_column_input(user_input, cols):
            # Invalid format or out of bounds
            continue
        col = ord(user_input) - ord('A')
        return col


def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = PLAYERS[current_player_idx]
        col = get_player_input(checker, COLS)

        if not has_space_in_column(board, col):
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        place_checker(board, col, checker)
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if is_board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
