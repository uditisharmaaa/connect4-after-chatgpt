import os
import random
import string

# ====== Configuration Constants ======
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
TOKENS = ["X", "O", "V", "H", "M"]  # In order

WIN_LENGTH = 4  # Always 4 to win as per assignment

# ====== Validation for constants ======
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")
if NUM_PLAYERS > len(TOKENS):
    raise ValueError("Not enough tokens for number of players.")

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]


# ====== Board Utilities ======
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    os.system('clear')


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


def is_valid_column_letter(s, cols):
    if len(s) != 1:
        return False
    if s not in string.ascii_uppercase:
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < cols


def column_full(board, col):
    return board[0][col] != " "


def drop_checker(board, col, token):
    # Place token in lowest available position in column col
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None  # Column full (should be checked before)


def board_full(board):
    return all(board[0][c] != " " for c in range(len(board[0])))


# ====== Win Checking ======
def check_win_from_cell(board, r, c, token, dr, dc):
    rows = len(board)
    cols = len(board[0])
    for k in range(WIN_LENGTH):
        rr = r + dr * k
        cc = c + dc * k
        if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
            return False
        if board[rr][cc] != token:
            return False
    return True


def has_won(board, token):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                if check_win_from_cell(board, r, c, token, dr, dc):
                    return True
    return False


# ====== Game Loop ======
def main():
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    print_board(board)

    while True:
        token = PLAYER_TOKENS[current_player_idx]

        # Before asking move, check if draw (safety)
        if board_full(board):
            print("It's a draw!")
            break

        # Prompt and validate input (only input validity, not column fullness)
        while True:
            user_input = input(f"Player {token}, please enter a column: ").strip().upper()
            if is_valid_column_letter(user_input, COLS):
                break
            else:
                print("Invalid input. Please enter a valid column letter.")

        col = ord(user_input) - ord('A')

        # If column is full, the player loses the turn
        if column_full(board, col):
            # Print updated board (unchanged) before passing turn, as per assignment style
            print_board(board)
            print(f"Column {user_input} is full. Player {token} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the checker
        drop_checker(board, col, token)

        # Print updated board
        print_board(board)

        # Check for win
        if has_won(board, token):
            print(f"Player {token} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
