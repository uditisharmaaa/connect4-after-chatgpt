import os
import random
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26 supported
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]  # In order for up to 5 players


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, current_checker):
    clear_screen()
    cols = len(board[0])
    # Header
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(header_letters))
    # Separator line
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)
    print(f"Player {current_checker}, please enter a column:")


def get_column_input(valid_cols):
    while True:
        user_input = sys.stdin.readline()
        if not user_input:
            return None  # EOF
        user_input = user_input.strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter for the column.")
            continue
        if user_input not in valid_cols:
            print("Invalid column. Please enter a valid column letter.")
            continue
        return valid_cols.index(user_input)


def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the given column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, last_r, last_c, checker):
    # Check 4 in a row in all directions from the last placed checker
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Check one direction
        r, c = last_r + dr, last_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def check_draw(board):
    # Draw if no spaces left in top row (or anywhere)
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Limit checks
    if COLS > 26:
        print("Maximum supported columns is 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Prepare column labels
    col_labels = [chr(ord('A') + i) for i in range(COLS)]

    # Choose random starting player
    current_index = random.randrange(NUM_PLAYERS)
    current_checker = players[current_index]

    # Initial board print
    print_board(board, current_checker)

    while True:
        # Get input
        col = get_column_input(col_labels)
        if col is None:
            print("Input ended. Exiting game.")
            return

        # Try to drop checker
        pos = drop_checker(board, col, current_checker)
        if pos is None:
            # Column full: player loses the turn
            print("Column is full. Turn lost.")
            # Print board for next player (unchanged)
            # Switch player
            current_index = (current_index + 1) % NUM_PLAYERS
            current_checker = players[current_index]
            print_board(board, current_checker)
            continue

        last_r, last_c = pos

        # Check for win
        if check_win(board, last_r, last_c, current_checker):
            # Print final board and announce winner
            clear_screen()
            # Print final board without extra prompt
            cols = len(board[0])
            header_letters = [chr(ord('A') + i) for i in range(cols)]
            print("  " + "   ".join(header_letters))
            sep = "+" + "+".join(["---"] * cols) + "+"
            for r in range(len(board)):
                print(sep)
                row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
                print(row_cells)
            print(sep)
            print(f"Player {current_checker} won!")
            return

        # Check for draw
        if check_draw(board):
            clear_screen()
            cols = len(board[0])
            header_letters = [chr(ord('A') + i) for i in range(cols)]
            print("  " + "   ".join(header_letters))
            sep = "+" + "+".join(["---"] * cols) + "+"
            for r in range(len(board)):
                print(sep)
                row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
                print(row_cells)
            print(sep)
            print("The game is a draw.")
            return

        # Switch player and print updated board
        current_index = (current_index + 1) % NUM_PLAYERS
        current_checker = players[current_index]
        print_board(board, current_checker)


if __name__ == "__main__":
    main()
