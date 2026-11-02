import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
VALID_COLUMNS = [chr(ord('A') + i) for i in range(COLS)]

NUM_PLAYERS = 2  # Set to 2 players as per submission requirement


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    # Print the board rows with separators
    sep = "+" + "---+" * len(board[0])
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)


def is_valid_column(col):
    return col in VALID_COLUMNS


def get_column_index(col):
    return ord(col) - ord('A')


def place_checker(board, col_idx, checker):
    # Place checker at the lowest empty position in col_idx
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    return -1  # column full


def check_win(board, row, col, checker):
    # Check all directions for a win of length WIN_LENGTH
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count the placed checker

        # check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def input_column(player_checker):
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col) != 1 or not is_valid_column(col):
            # Invalid input
            continue
        return col


def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_idx]

        col = input_column(checker)
        col_idx = get_column_index(col)
        row_idx = place_checker(board, col_idx, checker)

        if row_idx == -1:
            # Column full; player loses the turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, row_idx, col_idx, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
