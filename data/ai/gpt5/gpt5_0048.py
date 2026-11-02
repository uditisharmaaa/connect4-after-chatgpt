import os
import random
import sys

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LEN = 4

CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, col_labels):
    clear_screen()
    header = "  " + "   ".join(col_labels)
    print(header)
    horiz = "+" + "+".join(["---"] * len(col_labels)) + "+"
    for r in range(len(board)):
        print(horiz)
        row_cells = "| " + " | ".join(board[r]) + " |"
        print(row_cells)
    print(horiz)


def drop_piece(board, col, symbol):
    # Drops piece into the lowest available row in given column.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, row, col, symbol, need):
    rows = len(board)
    cols = len(board[0])

    def count_dir(dr, dc):
        cnt = 0
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            cnt += 1
            r += dr
            c += dc
        return cnt

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
        if total >= need:
            return True
    return False


def is_draw(board):
    for r in board:
        for cell in r:
            if cell == " ":
                return False
    return True


def get_valid_column_input(col_labels):
    # Keep asking until a valid column letter is provided (existing column)
    while True:
        try:
            user_in = input().strip().upper()
        except EOFError:
            sys.exit(0)
        if len(user_in) != 1 or not user_in.isalpha():
            print("Invalid input. Please enter a single letter for a column:")
            continue
        idx = ord(user_in) - ord('A')
        if 0 <= idx < len(col_labels):
            return idx
        else:
            print(f"Invalid column. Please choose between {col_labels[0]} and {col_labels[-1]}:")


def main():
    # Basic validations
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS > 26:
        print("COLS must be at most 26.")
        return

    board = create_board(ROWS, COLS)
    col_labels = [chr(ord('A') + i) for i in range(COLS)]
    player_symbols = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player and show initial board
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(board, col_labels)

    while True:
        print(f"Player {player_symbols[current]}, please enter a column:")
        col = get_valid_column_input(col_labels)

        placed_row = drop_piece(board, col, player_symbols[current])
        if placed_row is None:
            # Column full; turn lost
            print(f"Column {col_labels[col]} is full. Turn lost. Press Enter to continue...")
            try:
                input()
            except EOFError:
                pass
            # Next player's turn
            current = (current + 1) % NUM_PLAYERS
            print_board(board, col_labels)
            continue

        # After placing, check for win or draw
        if check_win(board, placed_row, col, player_symbols[current], WIN_LEN):
            print_board(board, col_labels)
            print(f"Player {player_symbols[current]} won!")
            break

        if is_draw(board):
            print_board(board, col_labels)
            print("Draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS
        print_board(board, col_labels)


if __name__ == "__main__":
    main()
