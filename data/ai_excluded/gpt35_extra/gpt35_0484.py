import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board with row separators
    for r in range(ROWS):
        print("+---" * COLUMNS + "+")
        row_str = "|"
        for c in range(COLUMNS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * COLUMNS + "+")

def get_valid_input(board, player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # invalid length
            continue
        if col_input not in COLUMN_LABELS:
            # not in board columns
            continue
        col_idx = COLUMN_LABELS.index(col_input)
        # check if column is full
        if board[0][col_idx] != " ":
            # column full - player loses turn
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker in lowest empty spot in the column
    for r in reversed(range(ROWS)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    # Should never get here if checked before
    return None, None

def check_win(board, checker, row, col):
    # Directions to check (delta_row, delta_col)
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYER_COUNT]

    # Randomly select first player index
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        col_idx = get_valid_input(board, current_checker)
        if col_idx is None:
            # column full -> turn lost
            current_player_idx = (current_player_idx + 1) % PLAYER_COUNT
            continue

        row_idx, _ = place_checker(board, col_idx, current_checker)

        clear_screen()
        print_board(board)

        if check_win(board, current_checker, row_idx, col_idx):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT


if __name__ == "__main__":
    main()
