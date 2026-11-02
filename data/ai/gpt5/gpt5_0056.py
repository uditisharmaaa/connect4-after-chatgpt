import os
import random
import sys

# ====== Configuration (change these constants for different games) ======
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
TOKENS_ALL = ["X", "O", "V", "H", "M"]
CONNECT_N = 4
# ========================================================================

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("COLS must be <= 26 (due to column letter labeling).")
    sys.exit(1)
TOKENS = TOKENS_ALL[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A.. up to number of columns
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    # Print the board in the specified format
    labels = column_labels(len(board[0]))
    # Header with column labels
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row_cells = "|" + "|".join(f" {cell} " for cell in board[r]) + "|"
        print(row_cells)
        print(sep)


def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    if not s.isalpha() or not s.isupper():
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < cols


def place_checker(board, col_index, token):
    # Place token in the lowest available row in the column.
    # Return the (row_index, col_index) if placed, else None if column full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = token
            return (r, col_index)
    return None


def check_direction(board, start_r, start_c, dr, dc, token, need):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    for k in range(need):
        rr = r + k * dr
        cc = c + k * dc
        if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
            return False
        if board[rr][cc] != token:
            return False
    return True


def check_win(board, token, need=CONNECT_N):
    rows = len(board)
    cols = len(board[0])
    # Directions: right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, token, need):
                    return True
    return False


def board_is_full(board):
    # If top row has any empty cell, board not full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def game_loop():
    board = create_board(ROWS, COLS)
    labels = column_labels(COLS)

    # Randomize starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial screen
    clear_screen()
    print_board(board)

    winner = None
    draw = False

    while True:
        # Show current board and prompt
        current_token = TOKENS[current_player_index]
        print(f"Player {current_token}, please enter a column:")

        # Read and validate input (invalid input -> ask again; turn not lost)
        col_input = ""
        while True:
            try:
                col_input = input().strip().upper()
            except EOFError:
                # Graceful exit if input unavailable
                print("\nInput closed. Exiting game.")
                return
            if is_valid_column_input(col_input, COLS):
                break
            else:
                print(f"Invalid input. Please enter a column letter between {labels[0]} and {labels[-1]} (uppercase).")

        col_index = ord(col_input) - ord('A')

        # Try to place checker; if column full, player loses turn
        placed = place_checker(board, col_index, current_token)
        if placed is None:
            # Column full: lose turn
            clear_screen()
            print_board(board)
            print(f"Column {col_input} is full. Player {current_token} loses the turn.")
            # Check for draw (board could be full)
            if board_is_full(board):
                draw = True
                break
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After a successful move, check for win/draw
        clear_screen()
        print_board(board)

        if check_win(board, current_token, CONNECT_N):
            winner = current_token
            break

        if board_is_full(board):
            draw = True
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game ended: announce result
    if winner is not None:
        print(f"Player {winner} won!")
    elif draw:
        print("The game is a draw.")


if __name__ == "__main__":
    game_loop()
