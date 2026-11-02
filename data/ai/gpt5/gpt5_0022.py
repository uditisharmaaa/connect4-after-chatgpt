import os
import random
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Checker symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))

    # Top border
    print("+" + ("---+" * cols))

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print("+" + ("---+" * cols))


def get_column_input(current_player_checker, cols):
    # Keep asking until a valid column letter is provided (input validation only)
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if user_input < 'A' or user_input > chr(ord('A') + cols - 1):
            print("Invalid column. Please enter a valid column letter within the board.")
            continue
        return ord(user_input) - ord('A')


def drop_checker(board, col, checker):
    # Attempt to place checker in the lowest empty cell of the given column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r
    return False, None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, last_row, last_col, checker):
    # Check 4 in a row including the last placed checker
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 1  # include last move
        # forward
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        return count

    # Directions: horizontal, vertical, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if count_direction(dr, dc) >= 4:
            return True
    return False


def is_draw(board):
    # Draw if no spaces left
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Basic validations for constants
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly choose starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_index]

        # Get a valid column letter input
        col = get_column_input(current_checker, COLS)

        # Attempt to drop checker
        success, row_placed = drop_checker(board, col, current_checker)

        # Clear and print updated board
        clear_screen()
        print_board(board)

        if not success:
            # Column full -> turn lost
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) through% NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, row_placed, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
