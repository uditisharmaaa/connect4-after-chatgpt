import os
import random
import sys

# Configuration constants (submission requires 6 rows x 7 cols and 2 players)
ROWS = 6
COLS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def in_bounds_col(col_char, cols):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + cols - 1)):
        return False
    return True

def drop_checker(board, col_idx, symbol):
    # Place in lowest available row in this column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == EMPTY:
            board[r][col_idx] = symbol
            return r
    return None  # Column full

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r][c+1] == symbol and
                board[r][c+2] == symbol and board[r][c+3] == symbol):
                return True

    # Vertical
    for r in range(rows - 3):
        for c in range(cols):
            if (board[r][c] == symbol and board[r+1][c] == symbol and
                board[r+2][c] == symbol and board[r+3][c] == symbol):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r+1][c+1] == symbol and
                board[r+2][c+2] == symbol and board[r+3][c+3] == symbol):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r-1][c+1] == symbol and
                board[r-2][c+2] == symbol and board[r-3][c+3] == symbol):
                return True

    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def prompt_for_column(cols, current_symbol):
    while True:
        try:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        except EOFError:
            # In case of non-interactive EOF, quit gracefully
            sys.exit(0)
        if in_bounds_col(user_input, cols):
            return ord(user_input) - ord('A')
        # Invalid input, ask again without losing the turn

def run_game():
    # Basic validations
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    clear_screen()
    print_board(board)

    while True:
        # Check draw before asking for a move (in case the board is full)
        if check_draw(board):
            print("It's a draw!")
            break

        current_symbol = players[current_player_idx]
        col_idx = prompt_for_column(COLS, current_symbol)

        # Attempt to drop the checker
        row = drop_checker(board, col_idx, current_symbol)
        if row is None:
            # Column full: lose the turn
            print(f"Column {chr(ord('A') + col_idx)} is full. Turn is lost.")
            # Next player
            current_player_idx = (current_player_idx + 1) * 1 % NUM_PLAYERS
            continue

        # Valid move: clear screen and print updated board
        clear_screen()
        print_board(board)

        # Check for a win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    run_game()
