import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

# For submission: 2 players, 6 rows, 7 columns
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

assert 1 <= ROWS <= 100  # sanity check, not necessary
assert 1 <= COLUMNS <= MAX_COLUMNS
assert MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    # Board[row][col], row 0 top, row rows-1 bottom
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for c in range(len(board[0])):
        header += f"  {chr(ord('A') + c)} "
    print(header)
    # Print horizontal separator line
    separator = "+" + "---+" * len(board[0])
    # Print rows
    for row in range(len(board)):
        print(separator)
        row_str = "|"
        for col in range(len(board[0])):
            row_str += f" {board[row][col]} |"
        print(row_str)
    print(separator)

def input_column(player_char, columns, board):
    valid_cols = [chr(ord("A") + i) for i in range(columns)]
    while True:
        user_input = input(f"Player {player_char}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + columns - 1)}.")
            continue
        if user_input not in valid_cols:
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + columns - 1)}.")
            continue
        col_index = ord(user_input) - ord("A")
        # Check if column full
        if board[0][col_index] != " ":
            # Full column, lose turn
            print(f"Column {user_input} is full. Turn lost.")
            return None
        else:
            return col_index

def place_checker(board, col, checker):
    # place checker in lowest available row in col
    for row in reversed(range(len(board))):  # bottom to top
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    return None  # column full (shouldn't happen if input_column handles it)

def check_win(board, checker, last_row, last_col):
    # Directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # If any top cell is empty, board not full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_char = players[current_player_idx]
        col = input_column(player_char, COLUMNS, board)
        if col is None:
            # lost turn due to full column
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        pos = place_checker(board, col, player_char)
        print_board(board)

        if check_win(board, player_char, pos[0], pos[1]):
            print(f"Player {player_char} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
