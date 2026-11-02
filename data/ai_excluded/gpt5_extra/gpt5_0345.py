import os
import random
import sys

# Constants (adjustable, but keep these for submission)
ROWS = 6
COLS = 7  # Max 26
PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(rows):
        line = "|"
        for c in range(cols):
            line += f" {board[r][c]} |"
        print(line)
        print("+" + ("---+" * cols))

def in_bounds_col(col_index):
    return 0 <= col_index < COLS

def letter_to_col(letter):
    if len(letter) != 1:
        return None
    if not letter.isalpha():
        return None
    letter = letter.upper()
    index = ord(letter) - ord('A')
    if 0 <= index < COLS:
        return index
    return None

def get_lowest_empty_row(board, col):
    # Returns row index where checker will land, or None if column is full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is None:
        return None
    board[row][col] = checker
    return row

def check_direction(board, start_r, start_c, delta_r, delta_c, checker):
    count = 0
    r, c = start_r, start_c
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        if count == WIN_LENGTH:
            return True
        r += delta_r
        c += delta_c
    return False

def check_win(board, checker):
    # Check all positions for a winning line starting at that position
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            # Right
            if c + (WIN_LENGTH - 1) < COLS and check_direction(board, r, c, 0, 1, checker):
                return True
            # Down
            if r + (WIN_LENGTH - 1) < ROWS and check_direction(board, r, c, 1, 0, checker):
                return True
            # Down-Right
            if (r + (WIN_LENGTH - 1) < ROWS) and (c + (WIN_LENGTH - 1) < COLS) and check_direction(board, r, c, 1, 1, checker):
                return True
            # Down-Left
            if (r + (WIN_LENGTH - 1) < ROWS) and (c - (WIN_LENGTH - 1) >= 0) and check_direction(board, r, c, 1, -1, checker):
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def get_player_input(current_checker):
    while True:
        try:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)
        if len(user_input) != 1:
            print("Invalid input. Enter a single uppercase letter corresponding to a column.")
            continue
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-Z).")
            continue
        col = letter_to_col(user_input.upper())
        if col is None:
            print("Invalid column. Please choose a valid column within the board.")
            continue
        return col

def main():
    # Basic validations for constants
    if not (2 <= PLAYERS <= 5):
        print("PLAYERS must be between 2 and 5.")
        return
    if COLS > 26:
        print("Maximum number of columns is 26.")
        return
    if ROWS <= 0 or COLS <= 0:
        print("ROWS and COLS must be positive.")
        return

    # Setup
    board = create_board(ROWS, COLS)
    player_checkers = CHECKERS[:PLAYERS]
    current_player = random.randrange(PLAYERS)

    # Initial board print
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        checker = player_checkers[current_player]
        col = get_player_input(checker)

        # Try placing checker
        row = place_checker(board, col, checker)
        if row is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {checker} loses the turn.")
            current_player = (current_player + 1) % PLAYERS
            # Check for draw (unlikely to be needed here, but safe)
            if board_full(board):
                print("It's a draw!")
                break
            continue

        # Successful move: update screen and check results
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
