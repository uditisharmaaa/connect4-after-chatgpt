import os
import random

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Validation for constraints
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")
if NUM_PLAYERS > len(PLAYER_TOKENS):
    raise ValueError("Not enough tokens for the number of players.")

TOKENS_IN_PLAY = PLAYER_TOKENS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(rows):
        row_line = "|"
        for c in range(cols):
            row_line += f" {board[r][c]} |"
        print(row_line)
        print("+" + ("---+" * cols))


def get_column_input(cols, current_token):
    valid_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        try:
            user_input = input(f"Player {current_token}, please enter a column: ").strip()
        except EOFError:
            # If input is not available, gracefully exit
            print("\nInput closed. Exiting game.")
            raise SystemExit(0)
        if len(user_input) != 1:
            continue
        letter = user_input.upper()
        if letter in valid_letters:
            return ord(letter) - ord('A')
        # Invalid input; loop continues until a valid column letter is given.


def place_checker(board, col, token):
    # Place from bottom to top
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return r, col
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, token):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_win_from(board, r, c, token):
    # Count in both directions for each axis; subtract 1 to avoid double-counting center
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = (
            check_direction(board, r, c, dr, dc, token) +
            check_direction(board, r, c, -dr, -dc, token) - 1
        )
        if total >= 4:
            return True
    return False


def is_draw(board):
    # Draw if no spaces in top row (or anywhere)
    for row in board:
        if ' ' in row:
            return False
    return True


def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players


def main():
    random.seed()  # Initialize RNG
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    print_board(board)

    while True:
        current_token = TOKENS_IN_PLAY[current_player_idx]
        # Prompt for a valid column letter
        col = get_column_input(COLS, current_token)

        # Attempt to place checker
        placement = place_checker(board, col, current_token)

        # After any change or even failed placement, print updated board as per requirements
        print_board(board)

        if placement is None:
            # Column is full; player loses the turn
            # Proceed to next player
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            continue

        r, c = placement

        # Check for win from the last placed position
        if check_win_from(board, r, c, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if is_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)


if __name__ == "__main__":
    main()
