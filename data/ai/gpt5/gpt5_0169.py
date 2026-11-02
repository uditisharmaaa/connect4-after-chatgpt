import os
import random
import string

# Constants (you may change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # 2 to 5

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

WIN_CONSECUTIVE = 4  # Always 4 to win


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = list(string.ascii_uppercase[:cols])
    header = "  " + "   ".join(letters)
    print(header)

    # Top border
    print("+" + "---+" * cols)

    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)


def column_letter_to_index(letter):
    letter = letter.upper()
    if len(letter) != 1:
        return None
    if letter < 'A' or letter >= chr(ord('A') + COLS):
        return None
    return ord(letter) - ord('A')


def get_lowest_empty_row(board, col):
    # Returns the row index where the checker will land, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is None:
        return None  # Column full
    board[row][col] = checker
    return row, col


def count_direction(board, start_r, start_c, dr, dc, checker):
    r = start_r + dr
    c = start_c + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, checker):
    # Check 4 directions: horizontal, vertical, diag1, diag2
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # include the last placed checker
        total += count_direction(board, last_r, last_c, dr, dc, checker)
        total += count_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= WIN_CONSECUTIVE:
            return True
    return False


def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Basic validation for constants
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        checker = CHECKERS[current_player_index]
        # Prompt input until valid column letter
        while True:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            col = column_letter_to_index(user_input)
            if col is not None:
                break  # valid input
            # Invalid input: keep asking (turn not lost)
            clear_screen()
            print_board(board)
            print("Invalid input. Please enter a valid column letter.")

        # Attempt to drop checker
        pos = drop_checker(board, col, checker)
        if pos is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full! Turn lost.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        last_r, last_c = pos

        # After placing, check for win or draw
        clear_screen()
        print_board(board)

        if check_win(board, last_r, last_c, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
