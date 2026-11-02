import os
import random
import string

# Constants (submission requires 6 rows x 7 cols and 2 players)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # supports 2..5

SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
LETTERS = string.ascii_uppercase[:COLS]


def clear_screen():
    os.system('clear')  # as required


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    # Header
    header = "  " + "   ".join(LETTERS[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
        print(sep)


def drop_checker(board, col, sym):
    # Place in lowest empty row; return (r,c) or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return (r, col)
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from(board, r, c):
    if r is None:
        return False
    sym = board[r][c]
    if sym == " ":
        return False
    rows, cols = len(board), len(board[0])
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for s in (1, -1):
            nr, nc = r + s * dr, c + s * dc
            while in_bounds(nr, nc, rows, cols) and board[nr][nc] == sym:
                count += 1
                if count >= 4:
                    return True
                nr += s * dr
                nc += s * dc
    return False


def is_draw(board):
    return all(cell != " " for row in board for cell in row)


def get_valid_column_input(prompt):
    while True:
        s = input(prompt).strip().upper()
        if len(s) != 1 or s not in LETTERS:
            print("Invalid input. Enter a single letter within the board (e.g., A, B, ...).")
            continue
        return LETTERS.index(s), s


def main():
    board = create_board(ROWS, COLS)
    player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board and starting player
    clear_screen()
    print_board(board)

    while True:
        sym = SYMBOLS[player_idx]
        print(f"Player {sym}, please enter a column:")
        col_idx, col_letter = get_valid_column_input("> ")

        pos = drop_checker(board, col_idx, sym)
        if pos is None:
            # Column full: lose turn
            clear_screen()
            print_board(board)
            print(f"Column {col_letter} is full. Player {sym} loses the turn.")
            player_idx = (player_idx + 1) % NUM_PLAYERS
            continue

        # Successful move: update screen
        clear_screen()
        print_board(board)

        if check_win_from(board, *pos):
            print(f"Player {sym} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        player_idx = (player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
