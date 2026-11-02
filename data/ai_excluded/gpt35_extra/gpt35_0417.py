import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for c in range(COLS):
        header += chr(ord('A') + c) + "   "
    print(header)
    # Print board rows
    for r in range(ROWS):
        line = "+"
        for _ in range(COLS):
            line += "---+"
        print(line)
        row_line = "|"
        for c in range(COLS):
            row_line += " " + board[r][c] + " |"
        print(row_line)
    print(line)

def get_column_index(input_str):
    if len(input_str) != 1:
        return -1
    c = input_str.upper()
    if 'A' <= c < chr(ord('A') + COLS):
        return ord(c) - ord('A')
    return -1

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    player_order = list(range(PLAYERS))
    current_player = random.choice(player_order)
    while True:
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")

        col_input = input().strip()
        col = get_column_index(col_input)

        if col == -1:
            # invalid input
            continue

        if is_column_full(board, col):
            # lose turn if column full
            current_player = (current_player + 1) % PLAYERS
            continue

        row, _ = place_checker(board, col, checker)
        if row == -1:
            # should not happen since checked full
            current_player = (current_player + 1) % PLAYERS
            continue

        if check_win(board, row, col, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if is_draw(board):
            print_board(board)
            print("Game ends in a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
