import os
import random
import sys

# Configuration constants
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate configuration
if COLS > 26:
    print("Error: COLS must be at most 26.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Print column headers
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print separator and rows
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)

def get_valid_column_input(player_symbol, cols):
    while True:
        user_in = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(user_in) != 1:
            continue
        if not user_in.isalpha():
            continue
        col_index = ord(user_in) - ord('A')
        if 0 <= col_index < cols:
            return col_index
        # otherwise loop again

def find_lowest_empty_row(board, col):
    # Returns the row index of the lowest empty cell in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, checker):
    row = find_lowest_empty_row(board, col)
    if row is None:
        return False
    board[row][col] = checker
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    needed = 4

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue

            # Horizontal right
            if c + needed - 1 < cols:
                ok = True
                for k in range(needed):
                    if board[r][c + k] != checker:
                        ok = False
                        break
                if ok:
                    return True

            # Vertical down
            if r + needed - 1 < rows:
                ok = True
                for k in range(needed):
                    if board[r + k][c] != checker:
                        ok = False
                        break
                if ok:
                    return True

            # Diagonal down-right
            if r + needed - 1 < rows and c + needed - 1 < cols:
                ok = True
                for k in range(needed):
                    if board[r + k][c + k] != checker:
                        ok = False
                        break
                if ok:
                    return True

            # Diagonal down-left
            if r + needed - 1 < rows and c - needed + 1 >= 0:
                ok = True
                for k in range(needed):
                    if board[r + k][c - k] != checker:
                        ok = False
                        break
                if ok:
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

    # Random starting player index
    current_index = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    print_board(board)

    while True:
        player = PLAYERS[current_index]

        # Ask for input (validated for form and range)
        col = get_valid_column_input(player, COLS)

        # Try to place; if column full, skip turn
        if not place_checker(board, col, player):
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {player} loses the turn.")
            # Move to next player
            current_index = (current_index + 1) % NUM_PLAYERS
            continue

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, player):
            print(f"Player {player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
