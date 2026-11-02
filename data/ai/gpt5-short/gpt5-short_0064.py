import os
import random
import sys

# ----------------------------
# Configuration (adjust these)
# ----------------------------
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"
TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5
CLEAR_CMD = "clear"  # Uses 'clear' as requested

# -------------
# Validations
# -------------
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

PLAYERS = TOKENS[:NUM_PLAYERS]


# -------------
# Board logic
# -------------
def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Column labels
    print("  " + "   ".join(list(COL_LABELS)))
    print(" +" + "---+" * COLS)

    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print(" | " + " | ".join(row_cells) + " |")
        print(" +" + "---+" * COLS)


def clear_screen():
    os.system(CLEAR_CMD)


def is_valid_column(board, col_index):
    if col_index < 0 or col_index >= COLS:
        return False
    # Valid if top cell of the column is empty
    return board[0][col_index] == ' '


def get_next_open_row(board, col_index):
    # Start from bottom row up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            return r
    return None  # Column full


def drop_token(board, row, col, token):
    board[row][col] = token


def is_draw(board):
    # Draw if no spaces left in the top row
    return all(board[0][c] != ' ' for c in range(COLS))


def winning_move(board, token):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == token and
                board[r][c + 1] == token and
                board[r][c + 2] == token and
                board[r][c + 3] == token):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == token and
                board[r + 1][c] == token and
                board[r + 2][c] == token and
                board[r + 3][c] == token):
                return True

    # Check positively sloped diagonals (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == token and
                board[r + 1][c + 1] == token and
                board[r + 2][c + 2] == token and
                board[r + 3][c + 3] == token):
                return True

    # Check negatively sloped diagonals (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == token and
                board[r - 1][c + 1] == token and
                board[r - 2][c + 2] == token and
                board[r - 3][c + 3] == token):
                return True

    return False


def prompt_for_column(current_token):
    while True:
        choice = input(f"Player {current_token}, choose a column (A-G): ").strip().upper()
        if len(choice) != 1 or choice not in COL_LABELS:
            print("Invalid input. Enter a single letter between A and G.")
            continue
        return COL_LABELS.index(choice)


def main():
    board = create_board()
    # Pick a random starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Game loop
    while True:
        clear_screen()
        current_token = PLAYERS[current_player_index]
        print(f"Connect 4 - {ROWS}x{COLS}  |  Players: {', '.join(PLAYERS)}")
        print(f"Current player: {current_token}")
        print_board(board)

        # Get a valid column from user
        col = prompt_for_column(current_token)
        if not is_valid_column(board, col):
            print("That column is full. Press Enter to try again.")
            input()
            continue

        # Place the token
        row = get_next_open_row(board, col)
        drop_token(board, row, col, current_token)

        # Check for win
        if winning_move(board, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
