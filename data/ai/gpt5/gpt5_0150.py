import random
import os
import string
import sys

# Constants (adjustable within constraints)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Up to 5 symbols

# Basic validations for constants
if COLS < 1 or COLS > 26:
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

# Slice symbols to the number of players
PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]


def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    # Initialize board with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Print column headers (A, B, C, ...)
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)

    # Print grid
    horiz = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(horiz)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(horiz)


def get_valid_column_input(prompt, cols):
    # Keep asking until a valid single-letter column within bounds is entered
    while True:
        col_in = input(prompt).strip()
        if len(col_in) != 1:
            print("Invalid input. Please enter a single uppercase letter for the column.")
            continue
        letter = col_in.upper()
        if letter < 'A' or letter >= chr(ord('A') + cols):
            print("Invalid column. Please enter a letter between A and " + chr(ord('A') + cols - 1) + ".")
            continue
        return ord(letter) - ord('A')


def find_drop_row(board, col):
    # Return the row index where the checker will land, or None if column is full
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    N = WIN_LENGTH

    # Directions: right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == N:
                        return True
                    rr += dr
                    cc += dc
    return False


def board_full(board):
    # If any top cell is empty, board is not full
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial print of board
    print_board(board)

    while True:
        current_symbol = PLAYERS[current_player_idx]
        prompt = f"Player {current_symbol}, please enter a column: "
        col = get_valid_column_input(prompt, COLS)

        drop_row = find_drop_row(board, col)
        if drop_row is None:
            # Column is full; turn lost
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
            input("Press Enter to continue...")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place the checker
        board[drop_row][col] = current_symbol

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
