import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4
MAX_COLS = 26
CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels (A, B, C, ...)
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print board with borders
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "| " + " | ".join(board[r]) + " |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def can_place_checker(board, col):
    return board[0][col] == " "

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot in column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full
    return None

def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]):
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r += delta_row
        c += delta_col
    return False

def check_all_directions(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontal for every row
    for r in range(rows):
        if check_line(board, r, 0, 0, 1, checker):
            return True

    # Check vertical for every column
    for c in range(cols):
        if check_line(board, 0, c, 1, 0, checker):
            return True

    # Check diagonals (top-left to bottom-right)
    # Start on top row and leftmost cols for diagonals
    for c in range(cols):
        if check_line(board, 0, c, 1, 1, checker):
            return True
    for r in range(1, rows):
        if check_line(board, r, 0, 1, 1, checker):
            return True

    # Check diagonals (top-right to bottom-left)
    for c in range(cols):
        if check_line(board, 0, c, 1, -1, checker):
            return True
    for r in range(1, rows):
        if check_line(board, r, cols - 1, 1, -1, checker):
            return True

    return False

def board_full(board):
    # If top row has no empty space, board is full
    return all(cell != " " for cell in board[0])

def ask_for_column(player_checker, cols, board):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(col_input, cols):
            # Invalid character or out of range
            continue
        col_idx = get_column_index(col_input)
        if not can_place_checker(board, col_idx):
            # Column full, player loses turn
            return None
        return col_idx

def main():
    # Set global constants per assignment submission instructions
    rows = ROWS
    cols = COLS
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]

    # Initialize board
    board = create_board(rows, cols)

    # Randomly select starting player
    current_player = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player_checker = checkers[current_player]
        col_idx = ask_for_column(player_checker, cols, board)

        if col_idx is None:
            # Column full, player loses turn
            current_player = (current_player + 1) % num_players
            continue

        place_checker(board, col_idx, player_checker)
        print_board(board)

        # Check win
        if check_all_directions(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
