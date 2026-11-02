import os
import random
import string

# Constants (submission must be 6 rows x 7 cols and 2 players)
ROWS = 6
COLS = 7  # maximum 26 supported
NUM_PLAYERS = 2  # between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # fixed at 4 per assignment


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Supports up to 26 columns (A-Z)
    labels = list(string.ascii_uppercase[:cols])
    return labels


def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    header = "  " + "   ".join(labels)
    print(header)
    # Top border line will be printed per row
    cols = len(board[0])
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    for r in range(len(board)):
        print(sep_line)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep_line)


def drop_checker(board, col_idx, checker):
    # Attempt to place checker in the lowest available row in col_idx
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    return None  # column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board, start_r, start_c, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for dr, dc in directions:
        count = 0
        r, c = start_r, start_c
        for _ in range(WIN_LENGTH):
            if in_bounds(r, c, rows, cols) and board[r][c] == checker:
                count += 1
                r += dr
                c += dc
            else:
                break
        if count == WIN_LENGTH:
            return True
    return False


def check_any_win(board):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            ch = board[r][c]
            if ch != " ":
                if check_win_from_cell(board, r, c, ch):
                    return ch
    return None


def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_valid_column_input(prompt, cols):
    labels = column_labels(cols)
    while True:
        user_in = input(prompt).strip()
        if len(user_in) != 1 or not user_in.isalpha():
            # invalid: not a single letter
            continue
        letter = user_in.upper()
        if letter in labels:
            return labels.index(letter)
        # else keep prompting until valid


def main():
    # Validate constraints
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if not (1 <= COLS <= 26):
        raise ValueError("COLS must be between 1 and 26.")

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    current_player_idx = random.randrange(NUM_PLAYERS)
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        col_idx = get_valid_column_input(prompt, COLS)

        placed = drop_checker(board, col_idx, current_checker)
        if placed is None:
            # Column is full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            # Optional feedback (not required, but helpful)
            # No additional printing before board per requirement; prompt next player on next loop
        else:
            # After successful placement, check for win
            winner = check_any_win(board)
            if winner:
                clear_screen()
                print_board(board)
                print(f"Player {winner} won!")
                break

            # Check draw
            if is_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break

            # Continue to next player
            clear_screen()
            print_board(board)

        # Advance to next player regardless of whether placement succeeded
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
