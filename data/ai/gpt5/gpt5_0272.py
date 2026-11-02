import os
import random
import sys

# ====== Configuration Constants ======
ROWS = 6            # Number of rows (e.g., 6)
COLS = 7            # Number of columns (e.g., 7) - maximum 26
NUM_PLAYERS = 2     # Number of players (between 2 and 5 inclusive)
WIN_LENGTH = 4      # Number of checkers in a row needed to win

CHECKERS = ["X", "O", "V", "H", "M"]  # Order of player checkers


# ====== Validation of Configuration ======
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("Maximum supported columns is 26.")
    sys.exit(1)

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


# ====== Game Functions ======
def clear_screen():
    # Clear screen for Unix/Linux terminals as required
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    if not s.isalpha() or not s.isupper():
        return False
    col_index = ord(s) - ord('A')
    return 0 <= col_index < cols


def get_lowest_empty_row(board, col):
    # Returns the row index where the checker should land, or -1 if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1


def drop_checker(board, col, symbol):
    row = get_lowest_empty_row(board, col)
    if row == -1:
        return -1
    board[row][col] = symbol
    return row


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_winner(board, symbol):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                    count += 1
                    if count >= WIN_LENGTH:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_draw(board):
    # A draw if there is no empty space in any column (i.e., top row has no spaces)
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def game_loop():
    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        symbol = PLAYER_SYMBOLS[current_player]
        prompt = f"Player {symbol}, please enter a column: "
        # Read and validate input (must be uppercase letter within bounds)
        while True:
            try:
                col_input = input(prompt).strip()
            except EOFError:
                print("\nInput closed. Exiting game.")
                return
            # Make it user-friendly: allow lowercase but validate to uppercase
            col_input = col_input.upper()

            if not is_valid_column_input(col_input, COLS):
                clear_screen()
                print_board(board)
                print("Invalid input. Please enter a valid uppercase column letter within the board.")
                continue
            break

        col = ord(col_input) - ord('A')
        placed_row = drop_checker(board, col, symbol)

        # Clear and print board after the attempted move
        clear_screen()
        print_board(board)

        if placed_row == -1:
            # Column full: player loses the turn
            print(f"Column {col_input} is full. Player {symbol} loses the turn.")
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_winner(board, symbol):
            print(f"Player {symbol} won!")
            return

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    game_loop()


if __name__ == "__main__":
    main()
