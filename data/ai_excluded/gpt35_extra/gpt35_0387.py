import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

NUM_PLAYERS = 2  # For submission, fixed to 2 players as per instructions


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    line_sep = "+" + "---+" * cols
    for r in range(rows):
        print(line_sep)
        row_str = "|"
        for c in range(cols):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print(line_sep)


def valid_input(user_input, cols):
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    if not ('A' <= ch <= chr(ord('A') + cols - 1)):
        return False
    return True


def get_column_index(user_input):
    return ord(user_input.upper()) - ord('A')


def place_checker(board, column, checker):
    """
    Place checker in the lowest available row in the given column.
    Returns True if placement was successful, False if column full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check diagonal down-right
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            found = True
            for i in range(WIN_LENGTH):
                if board[r + i][c + i] != checker:
                    found = False
                    break
            if found:
                return True

    # Check diagonal up-right
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            found = True
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] != checker:
                    found = False
                    break
            if found:
                return True

    return False


def check_draw(board):
    # If any cell is empty (" "), not a draw
    for row in board:
        if " " in row:
            return False
    return True


def main():
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        raise ValueError(f"NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}")

    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        user_input = input(prompt).strip()

        if not valid_input(user_input, COLS):
            # Invalid input, ask again (turn not lost)
            continue

        col_idx = get_column_index(user_input)

        if not place_checker(board, col_idx, current_checker):
            # Column full -> lose the turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After placing, check win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if check_draw(board):
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
