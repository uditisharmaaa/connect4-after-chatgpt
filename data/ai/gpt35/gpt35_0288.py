import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in range(ROWS):
        print("| " + " | ".join(board[row]) + " |")
        print("+" + "---+" * COLUMNS)


def get_player_input(player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLUMNS:
            continue
        return col


def place_checker(board, col, checker):
    # Place checker at lowest empty spot in column
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full


def is_winning_move(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1),  # diagonal down-left
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


def is_board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_index]

        col = get_player_input(checker)
        placed_row = place_checker(board, col, checker)

        if placed_row == -1:
            # Column full: player loses turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if is_winning_move(board, placed_row, col, checker):
            print(f"Player {checker} won!")
            break

        if is_board_full(board):
            print("Draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
