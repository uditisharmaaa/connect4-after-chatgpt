import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

# Players and their checkers
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

# Set game configuration here for submission
NUM_PLAYERS = 2  # For submission: 2 players
CHECKERS = PLAYERS_CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers (A, B, C, ...)
    headers = "  "
    for col in range(len(board[0])):
        headers += "  " + chr(ord('A') + col) + " "
    print(headers)
    # Print separator line
    sep_line = "+" + "---+" * len(board[0])
    # Print rows top to bottom
    print(sep_line)
    for row in range(len(board)):
        row_line = "|"
        for col in range(len(board[0])):
            row_line += " " + board[row][col] + " |"
        print(row_line)
        print(sep_line)

def is_valid_column(letter, cols):
    if len(letter) != 1:
        return False
    if not ('A' <= letter <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(letter, cols):
    return ord(letter) - ord('A')

def column_full(board, col_idx):
    # If topmost row in column is occupied, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    """
    Place checker in selected column.
    Checker falls to lowest empty row in that column.
    Returns True if placed successfully, False if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for row in range(rows):
        count = 0
        for col in range(cols):
            if board[row][col] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for col in range(cols):
        count = 0
        for row in range(rows):
            if board[row][col] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal check (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal check (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    # If any cell is empty, board is not full
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_valid_input(board, player_checker):
    cols = len(board[0])
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(inp, cols):
            continue
        col_idx = get_column_index(inp, cols)
        if column_full(board, col_idx):
            # Lose turn if column full, print no prompt here - as per spec player loses turn
            return None
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player_idx]

        col_idx = get_valid_input(board, checker)
        if col_idx is None:
            # Column full, player loses turn
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        place_checker(board, col_idx, checker)
        print_board(board)

        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
