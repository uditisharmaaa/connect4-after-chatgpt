import os
import random
import string
import sys

# =========================
# Configuration (Constants)
# =========================
ROWS = 6               # Number of rows (height)
COLS = 7               # Number of columns (width), must be <= 26
PLAYER_COUNT = 2       # Number of players, between 2 and 5 inclusive
TOKENS = ["X", "O", "V", "H", "M"]  # In order of assignment to players

# Safety checks for configuration
COLS = max(1, min(26, COLS))
PLAYER_COUNT = max(2, min(5, PLAYER_COUNT))
PLAYER_TOKENS = TOKENS[:PLAYER_COUNT]

# =========================
# Game Logic
# =========================

def clear_screen():
    # Clear the terminal screen (Unix/Linux)
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers
    header_letters = [string.ascii_uppercase[i] for i in range(cols)]
    header_line = "  " + "   ".join(header_letters)
    print(header_line)

    # Separator pattern
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c] if board[r][c] != " " else " ")
        print("| " + " | ".join(row_cells) + " |")
    print(sep)

def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    ch = s.upper()
    if ch < 'A' or ch > chr(ord('A') + cols - 1):
        return False
    return True

def col_letter_to_index(ch):
    return ord(ch.upper()) - ord('A')

def get_lowest_empty_row(board, col):
    # Start from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, col, token):
    row = get_lowest_empty_row(board, col)
    if row is None:
        return False
    board[row][col] = token
    return True

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    target = 4

    # Horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            count = count + 1 if board[r][c] == token else 0
            if count >= target:
                return True

    # Vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            count = count + 1 if board[r][c] == token else 0
            if count >= target:
                return True

    # Diagonal down-right (\)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            ok = True
            for k in range(1, target):
                rr = r + k
                cc = c + k
                if rr >= rows or cc >= cols or board[rr][cc] != token:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal up-right (/)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            ok = True
            for k in range(1, target):
                rr = r - k
                cc = c + k
                if rr < 0 or cc >= cols or board[rr][cc] != token:
                    ok = False
                    break
            if ok:
                return True

    return False

def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    status_message = ""

    # Initial board display before the game starts
    while True:
        clear_screen()
        print_board(board)
        if status_message:
            print(status_message)
            status_message = ""

        current_token = PLAYER_TOKENS[current_player_idx]
        prompt = f"Player {current_token}, please enter a column: "

        # Read and validate column input (keep asking until valid)
        while True:
            user_inp = input(prompt).strip().upper()
            if is_valid_column_input(user_inp, COLS):
                break
            else:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        col = col_letter_to_index(user_inp)

        # Try to drop checker; if column full, turn is lost
        placed = drop_checker(board, col, current_token)
        if not placed:
            status_message = f"Column {user_inp} is full. Turn lost."
        else:
            # Check for a win
            if check_win(board, current_token):
                clear_screen()
                print_board(board)
                print(f"Player {current_token} won!")
                break

        # Check for draw (board full)
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
