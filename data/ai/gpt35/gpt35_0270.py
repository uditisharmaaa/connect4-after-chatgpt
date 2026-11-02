import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord("A") + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print the board rows with separators
    for row in board:
        print("+" + "---+" * COLUMNS)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * COLUMNS)


def get_player_input(player, board):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # Input length invalid
            continue
        if col_input not in COLUMN_LABELS:
            # Input not in valid column labels
            continue
        col = COLUMN_LABELS.index(col_input)
        if board[0][col] != " ":
            # Column is full, player loses turn
            return None
        return col


def place_checker(board, col, checker):
    # Place checker in the lowest available space in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Should not reach here if called correctly


def check_win(board, checker, last_r, last_c):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check one direction
        r, c = last_r + dr, last_c + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = last_r - dr, last_c - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True

    return False


def check_draw(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_index]
        col = get_player_input(checker, board)

        if col is None:
            # Column full, lose turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        row, col = place_checker(board, col, checker)
        print_board(board)

        if check_win(board, checker, row, col):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
