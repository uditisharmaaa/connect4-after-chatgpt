import os
import random
import sys

# Constants (adjustable, but keep COLS <= 26)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]  # in order, up to 5 players


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    os.system('clear')


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Board grid
    for r in range(rows):
        print("+" + "---+" * cols)
        line = ""
        for c in range(cols):
            line += f"| {board[r][c]} "
        line += "|"
        print(line)
    print("+" + "---+" * cols)


def is_valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    ch = inp.upper()
    if ch < 'A' or ord(ch) >= ord('A') + cols:
        return False
    return True


def col_from_input(inp):
    return ord(inp.upper()) - ord('A')


def get_lowest_empty_row(board, col):
    # Returns the lowest available row index in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is None:
        return None
    board[row][col] = checker
    return row


def count_in_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r = start_r + dr
    c = start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win_from_cell(board, row, col, checker):
    # Check 4 in a row in any of 4 directions using the placed cell as center
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        total = 1  # count the placed checker
        total += count_in_direction(board, row, col, dr, dc, checker)
        total += count_in_direction(board, row, col, -dr, -dc, checker)
        if total >= 4:
            return True
    return False


def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Basic validations for constants
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Print initial empty board
    print_board(board)

    while True:
        # If board is full before a move, it's a draw
        if board_full(board):
            print("The game is a draw!")
            break

        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        # Get valid input (invalid input does not lose the turn)
        while True:
            user_input = input().strip()
            if is_valid_column_input(user_input, COLS):
                col = col_from_input(user_input)
                break
            else:
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}:")

        # Try to drop checker
        row = drop_checker(board, col, current_checker)
        if row is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            # Switch player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After a successful move, update display
        print_board(board)

        # Check for win
        if check_win_from_cell(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
