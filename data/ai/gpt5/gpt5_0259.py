import os
import random
import string
import sys

# ===============================
# Configuration (adjustable)
# ===============================
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # supported: 2 to 5
WIN_LENGTH = 4  # always 4 in a row to win (per assignment)

# Player tokens in order
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]


# ===============================
# Utilities
# ===============================
def clear_screen():
    # As per assignment, use 'clear'
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A, B, C, ... up to 26 max
    letters = list(string.ascii_uppercase)
    if cols > len(letters):
        raise ValueError("Maximum supported columns is 26.")
    return letters[:cols]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    clear_screen()

    # Header labels
    header = "  " + "   ".join(labels)
    print(header)

    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    # Rows
    for r in range(rows):
        print(border)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    # Bottom border
    print(border)


def get_players(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    return PLAYER_TOKENS[:num_players]


def is_valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    labels = column_labels(cols)
    return ch in labels


def col_index_from_label(label):
    return ord(label.upper()) - ord('A')


def find_available_row(board, col):
    # Return the lowest available row index in the column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def board_full(board):
    # If any top cell (row 0) has a space, not full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def check_win(board, last_r, last_c, token):
    # Check 4-in-a-row including position (last_r, last_c)
    # Directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1),  # diagonal /
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # count the last placed token

        # Go one way
        r, c = last_r + dr, last_c + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # Go the other way
        r, c = last_r - dr, last_c - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def prompt_input(prompt_text):
    try:
        return input(prompt_text)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting game.")
        sys.exit(0)


def main():
    # Setup
    board = create_board(ROWS, COLS)
    players = get_players(NUM_PLAYERS)
    current_player_idx = random.randrange(len(players))

    # Show initial empty board
    print_board(board)

    winner = None

    while True:
        current_token = players[current_player_idx]
        user_in = prompt_input(f"Player {current_token}, please enter a column: ").strip().upper()

        # Validate input (re-prompt until valid character)
        while not is_valid_column_input(user_in, COLS):
            print("Invalid input. Please enter a valid column letter.")
            user_in = prompt_input(f"Player {current_token}, please enter a column: ").strip().upper()

        col = col_index_from_label(user_in)

        # Try to place checker
        row = find_available_row(board, col)
        if row is None:
            # Column full: turn is lost
            print_board(board)
            print(f"Column {user_in} is full. Player {current_token} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) * 1 % len(players)
            continue

        # Place checker
        board[row][col] = current_token
        print_board(board)

        # Check for win
        if check_win(board, row, col, current_token):
            winner = current_token
            break

        # Check for draw
        if board_full(board):
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(players)

    # Game over
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
