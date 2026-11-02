# Connect 4 (6x7) for 2–5 players
# - Columns labeled A–G
# - Players use tokens X, O, V, H, M (configurable)
# - Random first player
# - Validates input and full columns
# - Detects wins and draws
# - Clears screen each turn with os.system('clear')

import os
import random
import sys

# -------------------- Configuration --------------------
ROWS = 6
COLS = 7

# Order of tokens available. Only first NUM_PLAYERS are used.
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Set the number of players here: must be 2–5
NUM_PLAYERS = 2

# -------------------------------------------------------


def clear_screen():
    # Use 'clear' (as requested). Fall back to 'cls' on Windows if needed.
    if os.system('clear') != 0:
        os.system('cls')


def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Column labels A–G
    headers = '  ' + '  '.join([chr(ord('A') + i) for i in range(COLS)])
    print(headers)
    print('+' + '---+' * COLS)
    for r in range(ROWS):
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
        print('+' + '---+' * COLS)


def get_valid_columns(board):
    # A column is valid if its top cell is empty
    valid = []
    for c in range(COLS):
        if board[0][c] == ' ':
            valid.append(c)
    return valid


def drop_token(board, col, token):
    # Drops token into the lowest empty row in the given column.
    # Returns (row_index, col) if successful, or None if column is full.
    if board[0][col] != ' ':
        return None
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return (r, col)
    return None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, last_r, last_c, token):
    # Check 4-in-a-row through last move in all 4 directions.
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        count = 1  # count the last placed token
        # forward direction
        r, c = last_r + dr, last_c + dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # backward direction
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False


def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))


def col_letter_to_index(letter):
    letter = letter.upper()
    if len(letter) != 1:
        return None
    if 'A' <= letter <= chr(ord('A') + COLS - 1):
        return ord(letter) - ord('A')
    return None


def prompt_for_column(board, token):
    valid_cols = get_valid_columns(board)
    valid_letters = {chr(ord('A') + c) for c in valid_cols}
    while True:
        choice = input(f"Player {token}, choose a column ({'/'.join(sorted(valid_letters))}): ").strip().upper()
        if choice == '':
            print("Please enter a column letter.")
            continue
        idx = col_letter_to_index(choice)
        if idx is None:
            print("Invalid input. Enter a single letter A–G corresponding to a column.")
            continue
        if idx not in valid_cols:
            print("That column is full or not available. Choose another.")
            continue
        return idx


def announce_players(tokens, start_index):
    order = tokens[start_index:] + tokens[:start_index]
    print("Players this game:", ' '.join(order))
    print(f"Randomly selected first player: {order[0]}")
    print()


def main():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_TOKENS):
        print("Error: Not enough PLAYER_TOKENS for the number of players.")
        sys.exit(1)

    tokens = PLAYER_TOKENS[:NUM_PLAYERS]

    board = create_board()
    start_index = random.randrange(NUM_PLAYERS)
    current_index = start_index

    # Initial screen
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Board size: {ROWS} rows x {COLS} columns (A–G)")
    announce_players(tokens, start_index)
    print_board(board)

    try:
        while True:
            token = tokens[current_index]

            # Prompt and place token
            col = prompt_for_column(board, token)
            result = drop_token(board, col, token)
            if result is None:
                # Should not happen due to validation
                print("Unexpected error: Column full. Try again.")
                continue
            last_r, last_c = result

            # Clear and reprint
            clear_screen()
            print_board(board)

            # Check for win
            if check_win(board, last_r, last_c, token):
                print(f"Player {token} wins! Four in a row.")
                break

            # Check for draw
            if board_full(board):
                print("It's a draw! No more moves available.")
                break

            # Next player's turn (cycle)
            current_index = (current_index + 1) % NUM_PLAYERS

    except (EOFError, KeyboardInterrupt):
        print("\nGame interrupted. Goodbye!")


if __name__ == "__main__":
    main()
