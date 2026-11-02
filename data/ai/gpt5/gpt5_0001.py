import os
import random
import string

# Constants (change these to test different setups; submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

EMPTY = " "
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Limit to 26 columns (A-Z)
    labels = list(string.ascii_uppercase[:min(cols, 26)])
    return labels


def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    print("  " + "   ".join(labels))
    # Rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = ""
        for c in range(len(board[0])):
            row_str += f"| {board[r][c]} "
        row_str += "|"
        print(row_str)
    print("+---" * len(board[0]) + "+")


def get_valid_input(prompt, valid_labels):
    while True:
        user_in = input(prompt).strip()
        if len(user_in) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        user_in = user_in.upper()
        if user_in not in valid_labels:
            print("Invalid column. Please enter a valid column letter on the board.")
            continue
        return user_in


def drop_checker(board, col_index, checker):
    # Drops checker into the lowest available row in the given column.
    # Returns the row index where the checker was placed, or None if column is full.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            board[row][col_index] = checker
            return row
    return None


def check_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    for _ in range(4):
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        else:
            break
    return count == 4


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check all cells as potential starting points
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Right
            if check_direction(board, r, c, 0, 1, checker):
                return True
            # Down
            if check_direction(board, r, c, 1, 0, checker):
                return True
            # Down-right
            if check_direction(board, r, c, 1, 1, checker):
                return True
            # Up-right
            if check_direction(board, r, c, -1, 1, checker):
                return True
    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def main():
    # Basic validations and setup
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    labels = column_labels(COLS)
    col_to_index = {label: i for i, label in enumerate(labels)}

    # Randomly select starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_index]
        # Display board and prompt
        print(f"Player {current_checker}, please enter a column:")
        # Get valid column label from user
        user_label = get_valid_input("", labels)
        col_idx = col_to_index[user_label]

        # Attempt to drop checker
        placed_row = drop_checker(board, col_idx, current_checker)
        if placed_row is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {user_label} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After a successful move, clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
