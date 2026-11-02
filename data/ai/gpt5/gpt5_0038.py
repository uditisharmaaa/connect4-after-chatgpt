import os
import random
import string

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])

    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Top border
    print("+" + "+".join(["---"] * cols) + "+")

    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "+".join(["---"] * cols) + "+")


def get_valid_input(cols):
    max_letter = chr(ord('A') + cols - 1)
    while True:
        entry = input(f"Please enter a column (A-{max_letter}): ").strip().upper()
        if len(entry) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        if entry < 'A' or entry > max_letter:
            print(f"Invalid column. Choose between A and {max_letter}.")
            continue
        return entry


def find_row_for_col(board, col):
    # Return the row index where the checker will land, or None if the column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_winner(board, symbol, last_r, last_c):
    # Check four directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count the last placed checker

        # Check one way
        r, c = last_r + dr, last_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Check the opposite way
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def main():
    if COLS > 26:
        print("Error: Maximum of 26 columns supported.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: Number of players must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {player_symbol}, please enter a column:")

        col_letter = get_valid_input(COLS)
        col_index = ord(col_letter) - ord('A')

        row_index = find_row_for_col(board, col_index)
        if row_index is None:
            # Column full: turn is invalid and is lost
            print(f"Column {col_letter} is full. Turn lost.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[row_index][col_index] = player_symbol

        # Check for win
        if check_winner(board, player_symbol, row_index, col_index):
            clear_screen()
            print_board(board)
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
