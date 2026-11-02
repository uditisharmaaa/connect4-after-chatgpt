import os
import random
import sys

# Constants (you may change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5

# Checker symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Ensure constraints
if COLS > 26:
    print("Maximum number of columns is 26.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Number of players must be between 2 and 5.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]


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

    horiz = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(horiz)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(horiz)


def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    ch = s.upper()
    if not ('A' <= ch <= 'Z'):
        return False
    idx = ord(ch) - ord('A')
    return 0 <= idx < cols


def input_column(prompt, cols):
    while True:
        val = input(prompt).strip().upper()
        if is_valid_column_input(val, cols):
            return ord(val) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter.")


def drop_checker(board, col, piece):
    # Drops piece into column; returns row index where placed, or None if column full
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = piece
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, piece):
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
            if board[r][c] != piece:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc, rows, cols) and board[rr][cc] == piece:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= 4:
                    return True
    return False


def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)

    # Randomly choose first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial print
    clear_screen()
    print_board(board)

    while True:
        piece = PLAYERS[current_player_index]
        print(f"Player {piece}, please enter a column:")
        col = input_column("> ", COLS)

        placed_row = drop_checker(board, col, piece)

        if placed_row is None:
            # Column full, turn lost
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {piece} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After a successful move, check for win or draw
        if check_win(board, piece):
            clear_screen()
            print_board(board)
            print(f"Player {piece} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next turn
        clear_screen()
        print_board(board)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
