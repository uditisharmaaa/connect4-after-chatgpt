import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LETTERS))
    # Print rows starting from top row (0) to bottom row (ROWS-1)
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        row_line = "|"
        for c in range(COLS):
            row_line += " " + board[r][c] + " |"
        print(row_line)
    print("+" + "---+" * COLS)


def input_column(player_checker, board):
    while True:
        col_in = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_in) != 1:
            # Invalid length
            continue
        if col_in not in COLUMN_LETTERS:
            # Invalid letter
            continue
        col_idx = COLUMN_LETTERS.index(col_in)
        # Check if the column is full
        if board[0][col_idx] != " ":
            # Column full, player loses turn
            return None
        return col_idx


def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty space in column col_idx
    # Rows from bottom (ROWS-1) upwards
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx  # Return position placed
    return None  # Should not happen if checked before


def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False


def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        col_idx = input_column(checker, board)

        if col_idx is None:
            # Full column - turn lost
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        row_idx, col_idx = place_checker(board, col_idx, checker)
        print_board(board)

        if check_win(board, row_idx, col_idx, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
