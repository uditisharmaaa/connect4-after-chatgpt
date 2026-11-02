import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

# Players setup
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

NUM_PLAYERS = 2  # Set to 2 as per submission instructions


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    rows = len(board)

    # Print column labels
    print(" ", end=" ")
    for i in range(cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print each row with separators
    for r in range(rows):
        print("+" + "---+" * cols)
        print("|", end="")
        for c in range(cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+" + "---+" * cols)


def valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    if letter < 'A' or letter >= chr(ord('A') + cols):
        return False
    return True


def get_column_index(letter):
    return ord(letter.upper()) - ord('A')


def place_checker(board, col_idx, checker):
    rows = len(board)
    # Place in the lowest empty row of the column
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    # Column full
    return None


def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(r_step, c_step):
        count = 1  # Current checker

        # Check one direction
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step

        # Check opposite direction
        r, c = row - r_step, col - c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= r_step
            c -= c_step

        return count

    # Horizontal check
    if count_direction(0, 1) >= WIN_LENGTH:
        return True
    # Vertical check
    if count_direction(1, 0) >= WIN_LENGTH:
        return True
    # Diagonal /
    if count_direction(1, 1) >= WIN_LENGTH:
        return True
    # Diagonal \
    if count_direction(1, -1) >= WIN_LENGTH:
        return True

    return False


def board_full(board):
    # If any cell in top row is empty, board is not full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def main():
    # Validate constants
    if not (4 <= WIN_LENGTH <= min(ROWS, COLS)):
        print("WIN_LENGTH constant invalid for board size.")
        return
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)

    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip()
            if not valid_column(user_input, COLS):
                # Invalid input: wrong length, invalid char, or out of range
                continue
            col_idx = get_column_index(user_input)
            placed = place_checker(board, col_idx, checker)
            if placed is None:
                # Column full - turn lost
                break
            else:
                row, col = placed
                break

        clear_screen()
        print_board(board)

        # If not placed (None), player loses turn, no win check
        if placed is not None:
            if check_win(board, row, col, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("The game is a draw.")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
