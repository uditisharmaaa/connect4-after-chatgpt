import os
import random
import string
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26 supported due to column labeling A-Z
NUM_PLAYERS = 2  # Between 2 and 5

# Player tokens in order
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']


def clear_screen():
    # Clear screen on Unix/Linux/macOS terminals
    os.system('clear')


def create_board(rows, cols):
    # Create a 2D board initialized with spaces " "
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])
    clear_screen()

    # Header row with column letters
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)

    # Top grid border
    print("+" + ("---+" * cols))

    # Rows (from top row to bottom row)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))


def is_input_valid(user_input, cols):
    # Validate input is a single letter within the column range
    if not user_input or len(user_input) != 1:
        return False
    ch = user_input.upper()
    if ch < 'A' or ch >= chr(ord('A') + cols):
        return False
    return True


def column_index_from_input(user_input):
    return ord(user_input.upper()) - ord('A')


def place_checker(board, col_index, token):
    # Attempt to place token in the lowest empty spot of col_index
    # Return True if placed, False if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = token
            return True
    return False


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                cnt = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token and cnt < 4:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= 4:
                    return True
    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def assert_parameters():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)


def main():
    assert_parameters()

    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial print of the empty board
    print_board(board)
    print(f"Player {tokens[current_player_idx]} starts.")

    while True:
        # Before asking for input, also check for draw (in case initial board is full in other configs)
        if board_full(board):
            print("It's a draw!")
            break

        # Prompt the current player
        current_token = tokens[current_player_idx]
        user_in = input(f"Player {current_token}, please enter a column: ").strip()

        # Validate input (repeat until syntactically valid; this does not include full column case)
        while not is_input_valid(user_in, COLS):
            print_board(board)
            print("Invalid input. Please enter a valid column letter.")
            user_in = input(f"Player {current_token}, please enter a column: ").strip()

        col_idx = column_index_from_input(user_in)

        # Try to place the checker
        placed = place_checker(board, col_idx, current_token)

        # Print board after attempt (updated or not)
        print_board(board)

        if not placed:
            # Column full: invalid move, turn is lost
            col_letter = chr(ord('A') + col_idx)
            print(f"Column {col_letter} is full. Invalid move: turn lost.")
            # Switch to next player
            current_player_idx = (current_player_idx + 1) * 1 % NUM_PLAYERS
            continue

        # After a successful move, check for win
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw after successful move
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
