import os
import random
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header
    letters = [chr(ord('A') + i) for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)
    print("+" + "---+" * cols)

    # Rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * cols)


def input_to_col(inp, cols):
    if not inp:
        return None
    s = inp.strip().upper()
    if len(s) != 1:
        return None
    if not ('A' <= s <= 'Z'):
        return None
    idx = ord(s) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None


def column_full(board, col):
    # If top cell of column is occupied, column is full
    return board[0][col] != " "


def place_checker(board, col, token):
    # Place token in the lowest available row in the given column.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return True
    return False


def check_winner(board, token):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - WIN_LEN + 1):
            if all(board[r][c + k] == token for k in range(WIN_LEN)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - WIN_LEN + 1):
            if all(board[r + k][c] == token for k in range(WIN_LEN)):
                return True

    # Diagonal down-right
    for r in range(rows - WIN_LEN + 1):
        for c in range(cols - WIN_LEN + 1):
            if all(board[r + k][c + k] == token for k in range(WIN_LEN)):
                return True

    # Diagonal up-right
    for r in range(WIN_LEN - 1, rows):
        for c in range(cols - WIN_LEN + 1):
            if all(board[r - k][c + k] == token for k in range(WIN_LEN)):
                return True

    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    # Basic validations for constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    board = create_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]

    # Randomly choose starting player
    current = random.randint(0, NUM_PLAYERS - 1)

    # Show empty board first
    print_board(board)

    while True:
        current_token = players[current]
        # Prompt until a valid column letter is provided
        while True:
            try:
                user_input = input(f"Player {current_token}, please enter a column: ")
            except EOFError:
                print("\nInput ended. Exiting game.")
                return
            col = input_to_col(user_input, COLS)
            if col is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
                continue
            # We have a valid column letter; proceed to attempt placement
            break

        if column_full(board, col):
            # Turn is invalid and lost
            print(f"Column {chr(ord('A') + col)} is full. You lose your turn.")
            current = (current + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place checker
        placed = place_checker(board, col, current_token)
        # placed should be True if not full; proceed
        print_board(board)

        # Check for win
        if check_winner(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
