import os
import random
import sys

# ----------------------------
# Constants (adjust as needed)
# ----------------------------
NUM_ROWS = 6
NUM_COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Allowed player symbols in the order you want to seat them by default
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# How many players are playing (must be between 2 and 5, inclusive)
NUM_PLAYERS = 2
# ----------------------------


def clear_screen():
    # The prompt requested os.system('clear')
    os.system('clear')


def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Print column headers
    print("  " + " ".join(COLUMN_LABELS))
    # Print rows
    for r in range(len(board)):
        row_str = [board[r][c] for c in range(len(board[0]))]
        print(str(len(board) - r) + " " + " ".join(row_str))
    # Bottom line (optional): repeat column headers
    print("  " + " ".join(COLUMN_LABELS))


def letter_to_col(letter):
    letter = letter.upper()
    if letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(letter)
    return None


def get_next_open_row(board, col):
    # Return the bottom-most empty row in a column, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def is_draw(board):
    # Draw if top row is completely full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, row, col, symbol):
    # Check all 4 directions that matter:
    # Horizontal (0,1), Vertical (1,0), Diagonal down-right (1,1), Diagonal up-right (-1,1)

    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # include the placed piece

        # forward direction
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # backward direction
        r, c = row - dr, col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def prompt_for_move(player_symbol, board):
    cols_text = f"({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]})"
    while True:
        choice = input(f"Player {player_symbol}, choose a column {cols_text}: ").strip().upper()
        # Validate input length and character
        if len(choice) != 1 or choice not in COLUMN_LABELS:
            print(f"Invalid input. Enter a single letter {cols_text}.")
            continue

        col = letter_to_col(choice)
        row = get_next_open_row(board, col)
        if row is None:
            print("That column is full. Choose another.")
            continue

        return row, col


def main():
    # Validate number of players
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5. Exiting.")
        sys.exit(1)

    # Select active players and randomize their order
    active_players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    random.shuffle(active_players)

    board = create_board()
    current_idx = 0

    while True:
        clear_screen()
        print_board(board)
        print(f"Turn order: {' '.join(active_players)}")
        current_player = active_players[current_idx]

        # Ask for and place move
        row, col = prompt_for_move(current_player, board)
        board[row][col] = current_player

        # Clear to show updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} wins!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % len(active_players)


if __name__ == "__main__":
    main()
