import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Set number of players here, must be between MIN_PLAYERS and MAX_PLAYERS
WIN_COUNT = 4

CHECKERS = ["X", "O", "V", "H", "M"]

assert MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS
assert COLS <= 26  # Columns limited by letters A-Z

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    header = "  "
    for i in range(cols):
        header += chr(ord('A') + i) + "   "
    print(header)
    separator = "+---" * cols + "+"
    for r in range(rows):
        print(separator)
        row_line = "|"
        for c in range(cols):
            row_line += ' {} |'.format(board[r][c])
        print(row_line)
    print(separator)

def valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    c = inp[0]
    if c < 'A' or c >= chr(ord('A') + cols):
        return False
    return True

def get_column_index(inp):
    return ord(inp) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available row in col_idx
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    return -1  # Column full

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    rows, cols = len(board), len(board[0])
    while 0 <= r < rows and 0 <= c < cols:
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r += delta_row
        c += delta_col
    return False

def check_win(board, row, col, checker):
    # Check horizontal
    if check_direction(board, row, 0, 0, 1, checker):
        return True
    # Check vertical
    if check_direction(board, 0, col, 1, 0, checker):
        return True
    # Check diagonal /
    # Go to bottom-left
    r, c = row, col
    while r < len(board) - 1 and c > 0:
        r += 1
        c -= 1
    if check_direction(board, r, c, -1, 1, checker):
        return True
    # Check diagonal \
    # Go to top-left
    r, c = row, col
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    if check_direction(board, r, c, 1, 1, checker):
        return True
    return False

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        print(f"Player {checker}, please enter a column:")
        inp = input().strip().upper()

        if not valid_column_input(inp, COLS):
            # Invalid input, ask again without losing turn
            continue

        col_idx = get_column_index(inp)
        placed_row = place_checker(board, col_idx, checker)

        if placed_row == -1:
            # Column full, player loses turn
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, placed_row, col_idx, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
