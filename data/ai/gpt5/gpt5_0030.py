import os
import random
import string

# -------------------- Configuration --------------------
ROWS = 6
COLS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
# -------------------------------------------------------

assert 2 <= NUM_PLAYERS <= 5
assert 1 <= COLS <= 26
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    # Requirement: clear screen using 'clear'
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    # Top border line
    border = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(border)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(border)


def column_from_input(user_input, cols):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    if user_input < 'A' or user_input >= chr(ord('A') + cols):
        return None
    return ord(user_input) - ord('A')


def drop_checker(board, col, checker):
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r = start_r + dr
    c = start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, checker):
    # Check 4 in a row using last placed position
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1
        total += count_in_direction(board, last_r, last_c, dr, dc, checker)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no empty spaces remain
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        checker = PLAYER_CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        # Read and validate input (keep asking until valid letter)
        col = None
        while col is None:
            try:
                user_in = input().strip()
            except EOFError:
                return
            col_candidate = column_from_input(user_in, COLS)
            if col_candidate is None:
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = col_candidate

        # Try to drop checker
        row_placed = drop_checker(board, col, checker)
        if row_placed is None:
            # Column full: player loses turn
            # Proceed to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, row_placed, col, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
