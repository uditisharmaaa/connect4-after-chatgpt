import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# For this assignment requirements:
NUM_PLAYERS = 2  # must be 2 for submission
BOARD_ROWS = 6   # must be 6 for submission
BOARD_COLS = 7   # must be 7 for submission

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers A, B, C, ...
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)
    print("+" + "---+" * cols)
    for row in range(len(board)):
        row_cells = "| " + " | ".join(board[row]) + " |"
        print(row_cells)
        print("+" + "---+" * cols)

def column_letter_to_index(c):
    if len(c) != 1:
        return -1
    uc = c.upper()
    idx = ord(uc) - ord('A')
    if 0 <= idx < BOARD_COLS:
        return idx
    return -1

def is_column_full(board, col):
    # If top row in column is occupied, it's full
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in lowest empty row in col
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check diagonal down-right (\)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal up-right (/)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    for c in range(len(board[0])):
        if not is_column_full(board, c):
            return False
    return True

def get_valid_input(player_checker, board):
    cols = len(board[0])
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(inp) != 1:
            # Invalid input length
            continue
        col_index = column_letter_to_index(inp)
        if col_index == -1:
            # Invalid column letter
            continue
        if is_column_full(board, col_index):
            # Column is full - player loses turn
            return None
        return col_index

def main():
    # Validate constants for assignment
    assert 2 <= NUM_PLAYERS <= 5
    assert BOARD_COLS <= MAX_COLS
    assert BOARD_ROWS > 0 and BOARD_COLS > 0

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(BOARD_ROWS, BOARD_COLS)

    # Random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]

        col_index = get_valid_input(current_checker, board)
        if col_index is None:
            # Column full - player loses turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        place_checker(board, col_index, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
