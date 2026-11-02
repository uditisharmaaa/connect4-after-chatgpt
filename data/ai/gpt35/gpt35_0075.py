import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4

CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Settings for this submission:
NUM_PLAYERS = 2


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print rows
    line = "+---" * cols + "+"
    for r in range(rows):
        print(line)
        row_str = "| " + " | ".join(board[r][c] for c in range(cols)) + " |"
        print(row_str)
    print(line)


def col_letter_to_index(letter, cols):
    if len(letter) != 1 or not ('A' <= letter <= chr(ord('A') + cols - 1)):
        return None
    return ord(letter) - ord('A')


def is_valid_column(col_idx, board):
    cols = len(board[0])
    rows = len(board)
    if col_idx is None or not (0 <= col_idx < cols):
        return False
    # If top row empty, column is not full
    return board[0][col_idx] == " "


def place_checker(board, col_idx, checker):
    rows = len(board)
    # Start from bottom row going upwards, find first empty cell in the column
    for r in reversed(range(rows)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    # If column full:
    return None, None


def check_win(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        return count

    # Directions: horizontal, vertical, diagonal \, diagonal /
    # Check horizontally
    horizontal = 1 + count_direction(0, -1) + count_direction(0, 1)
    if horizontal >= WIN_COUNT:
        return True

    # Check vertically
    vertical = 1 + count_direction(-1, 0) + count_direction(1, 0)
    if vertical >= WIN_COUNT:
        return True

    # Check diagonal \
    diag1 = 1 + count_direction(-1, -1) + count_direction(1, 1)
    if diag1 >= WIN_COUNT:
        return True

    # Check diagonal /
    diag2 = 1 + count_direction(-1, 1) + count_direction(1, -1)
    if diag2 >= WIN_COUNT:
        return True

    return False


def board_full(board):
    return all(cell != " " for cell in board[0])


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        print(f"Player {player_checker}, please enter a column:")
        valid_input = False
        col_idx = None
        while not valid_input:
            user_input = input().strip().upper()
            if len(user_input) == 0:
                print(f"Invalid input. Please enter a column letter (A-{chr(ord('A') + COLS - 1)}):")
                continue
            col_idx = col_letter_to_index(user_input, COLS)
            if col_idx is None:
                print(f"Invalid input. Please enter a column letter (A-{chr(ord('A') + COLS - 1)}):")
                continue
            if not is_valid_column(col_idx, board):
                # Column full: player loses turn
                print(f"Column {user_input} is full. You lose your turn.")
                col_idx = None
                valid_input = True  # To end input but no placement
                break
            valid_input = True

        if col_idx is not None:
            r, c = place_checker(board, col_idx, player_checker)
            print_board(board)
            if check_win(board, r, c, player_checker):
                print(f"Player {player_checker} won!")
                break
            if board_full(board):
                print("The game is a draw.")
                break
        else:
            # No placement done (column full). Just print board again
            print_board(board)
            if board_full(board):
                print("The game is a draw.")
                break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
