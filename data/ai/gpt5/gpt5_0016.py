import os
import random
import sys

# Constants (you may change these to test different configurations, but submit with these)
ROWS = 6
COLS = 7  # must be <= 26
NUM_PLAYERS = 2  # between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # Labels A, B, C, ... up to Z (max 26)
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    header = "  " + "   ".join(labels)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep_line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep_line)

def get_valid_column_input(num_cols, current_player_symbol):
    labels = column_labels(num_cols)
    label_set = set(labels)
    while True:
        try:
            user_in = input(f"Player {current_player_symbol}, please enter a column: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if len(user_in) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if user_in not in label_set:
            print(f"Invalid column. Please enter a letter between {labels[0]} and {labels[-1]}.")
            continue
        return labels.index(user_in), user_in  # return both index and label for messages

def drop_checker(board, col, symbol):
    # Place in lowest available row in this column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True
    return False  # column full

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc): right, down, diag down-right, diag down-left
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
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

def is_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Validate constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select starting player index
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_symbol = players[current_idx]
        # Prompt until valid column letter (range/format). Full column results in turn loss.
        col_idx, col_label = get_valid_column_input(COLS, current_symbol)

        # Attempt to drop checker
        placed = drop_checker(board, col_idx, current_symbol)

        # After each action, clear and print updated board
        clear_screen()
        print_board(board)

        if not placed:
            print(f"Column {col_label} is full. Turn lost.")
            # Advance to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Check win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
