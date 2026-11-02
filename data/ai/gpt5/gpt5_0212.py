import os
import random
import sys

# Configuration constants (submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Rows with grid
    horiz = "+" + "---+" * cols
    for r in range(rows):
        print(horiz)
        row_cells = "|"
        for c in range(cols):
            row_cells += f" {board[r][c]} |"
        print(row_cells)
    print(horiz)


def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    if not s.isalpha() or not s.isupper():
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < cols


def find_drop_row(board, col):
    # Return the row index where the checker will land, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, checker):
    r = find_drop_row(board, col)
    if r is None:
        return False
    board[r][col] = checker
    return True


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < WIN_COUNT and in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= WIN_COUNT:
                    return True
    return False


def check_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(i, total):
    return (i + 1) % total


def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {PLAYERS[current_player_idx]}, please enter a column:")
        # Read and validate input
        move = input().strip()
        # Keep asking until a valid column letter is provided
        while not is_valid_column_input(move, COLS):
            print("Invalid input. Please enter an uppercase letter within the board (e.g., A-G).")
            move = input().strip()

        col = ord(move) - ord('A')

        # Attempt to drop checker
        if not drop_checker(board, col, PLAYERS[current_player_idx]):
            # Column full: lose the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {PLAYERS[current_player_idx]} loses the turn.")
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            # Continue to next player's turn
            continue

        # After a successful move, check for win
        if check_win(board, PLAYERS[current_player_idx]):
            clear_screen()
            print_board(board)
            print(f"Player {PLAYERS[current_player_idx]} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)


if __name__ == "__main__":
    main()
