import os
import random

# -----------------------------
# Configuration (change if needed)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']
# -----------------------------

# Safety checks for configuration
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS < 1 or COLS > 26:
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    os.system('clear')


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Header with column letters
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    sep = "+" + "---+" * cols
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)


def find_lowest_empty_row(board, col):
    # returns row index to place, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1)   # down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                    count += 1
                    if count == WIN_LENGTH:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def get_column_from_input(user_input, cols):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    if not ('A' <= user_input <= 'Z'):
        return None
    col = ord(user_input) - ord('A')
    if col < 0 or col >= cols:
        return None
    return col


def main():
    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)

    while True:
        print_board(board)
        token = PLAYER_TOKENS[current_player]
        print(f"Player {token}, please enter a column:")

        # Get valid input (except full column which loses turn)
        col = None
        while True:
            user_in = input().strip()
            col = get_column_from_input(user_in, COLS)
            if col is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
                continue
            break

        row_to_place = find_lowest_empty_row(board, col)
        if row_to_place is None:
            # Column full: player loses the turn
            print(f"Column {chr(ord('A') + col)} is full. You lose your turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[row_to_place][col] = token

        # Check for win
        if check_win(board, token):
            print_board(board)
            print(f"Player {token} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("Game is a draw.")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
