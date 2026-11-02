import os
import random
import sys

# Constants
ROWS = 6
COLS = 7  # Max 26 supported
NUM_PLAYERS = 2  # Can be between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header with column letters
    header = "  " + "   ".join(LETTERS[:cols])
    print(header)
    # Top border and rows
    for r in range(len(board)):
        print("+---" * cols + "+")
        row_str = ""
        for c in range(cols):
            row_str += f"| {board[r][c]} "
        row_str += "|"
        print(row_str)
    print("+---" * cols + "+")

def get_valid_column_input(cols):
    while True:
        user_in = input().strip()
        if len(user_in) != 1:
            print("Invalid input. Please enter a single uppercase letter for the column:")
            continue
        ch = user_in.upper()
        if ch not in LETTERS[:cols]:
            print("Invalid input. Please enter a valid column letter within the board:")
            continue
        return LETTERS.index(ch)

def place_checker(board, col, checker):
    # Place checker in the lowest available row in the given column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column is full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    for _ in range(WIN_LENGTH):
        if in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        else:
            break
    return count == WIN_LENGTH

def check_win(board, r, c):
    checker = board[r][c]
    if checker == " ":
        return False
    # Directions: right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # To correctly count 4 in a row in any contiguous segment,
        # we step back up to 3 times opposite direction to get the minimal start
        start_r = r
        start_c = c
        for _ in range(WIN_LENGTH - 1):
            nr = start_r - dr
            nc = start_c - dc
            if in_bounds(nr, nc, len(board), len(board[0])) and board[nr][nc] == checker:
                start_r = nr
                start_c = nc
            else:
                break
        # Now check sequences of length 4 from the earliest start
        # Try up to 4 steps forward segments
        for offset in range(WIN_LENGTH):
            sr = start_r + offset * dr
            sc = start_c + offset * dc
            if check_direction(board, sr, sc, dr, dc, checker):
                return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        sys.exit(1)

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        col = get_valid_column_input(COLS)

        placement = place_checker(board, col, current_checker)
        if placement is None:
            # Column full; lose the turn
            print(f"Column {LETTERS[col]} is full. Turn lost.")
            # Press Enter to continue (optional, but keeps behavior clear)
            # input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Successfully placed
        r, c = placement
        clear_screen()
        print_board(board)

        if check_win(board, r, c):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
