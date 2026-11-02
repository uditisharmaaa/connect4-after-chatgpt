import os
import random
import sys

# -------------------- Configuration (change these to test other setups) --------------------
ROWS = 6
COLS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
# ------------------------------------------------------------------------------------------

assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
assert 1 <= COLS <= 26, "COLS must be between 1 and 26"
PLAYER_SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A..Z (up to 26)
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header
    print("  " + "   ".join(labels))
    # Top border
    print("+---" * cols + "+")

    # Board rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+---" * cols + "+")


def get_valid_column_input(prompt, cols):
    labels = column_labels(cols)
    while True:
        try:
            s = input(prompt)
        except EOFError:
            # Treat EOF as quit
            print("\nInput closed. Exiting game.")
            sys.exit(0)
        if not s:
            print("Invalid input. Please enter a column letter.")
            continue
        s = s.strip().upper()
        if len(s) != 1 or not ('A' <= s <= chr(ord('A') + cols - 1)):
            print("Invalid input. Please enter a valid column letter within the board.")
            continue
        return labels.index(s)


def find_lowest_empty_row(board, col):
    # Return the row index to place, or None if column full
    for r in reversed(range(len(board))):  # start from bottom
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, symbol):
    r = find_lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return r


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board, r, c, symbol):
    # Check 4 directions: horiz, vert, diag1, diag2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include placed checker
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False


def is_draw(board):
    # Draw if no empty cells remain
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    random.seed()
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player = random.randrange(NUM_PLAYERS)

    # Show initial board
    print_board(board)

    # Game loop
    while True:
        symbol = PLAYER_SYMBOLS[current_player]
        prompt = f"Player {symbol}, please enter a column: "
        col = get_valid_column_input(prompt, COLS)

        row = place_checker(board, col, symbol)
        if row is None:
            # Column full -> lose the turn
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {symbol} loses the turn.")
            # Next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # After a successful placement, print board and check game state
        print_board(board)

        if is_winning_move(board, row, col, symbol):
            print(f"Player {symbol} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
