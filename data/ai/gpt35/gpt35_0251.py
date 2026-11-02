import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COL_LABELS))
    # Print top border row
    print("+" + "---+" * COLS)
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(col_char):
    return col_char in COL_LABELS

def col_to_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Places a checker in the specified column if possible, 
    in the lowest available row.
    Returns True if placed, False if column is full.
    """
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # Column full

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    """
    Checks a line of length WIN_COUNT starting at (start_row, start_col)
    advancing by (delta_row, delta_col) each step.
    Returns True if all are the given checker.
    """
    for i in range(WIN_COUNT):
        r = start_row + i * delta_row
        c = start_col + i * delta_col
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
        if board[r][c] != checker:
            return False
    return True

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if check_line(board, r, c, 0, 1, checker):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if check_line(board, r, c, 1, 0, checker):
                return True

    # Diagonal down-right check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if check_line(board, r, c, 1, 1, checker):
                return True

    # Diagonal up-right check
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if check_line(board, r, c, -1, 1, checker):
                return True

    return False

def ask_player_for_column(player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            # Must be single uppercase letter
            continue
        if not is_valid_column(inp):
            continue
        return inp

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        col_char = ask_player_for_column(current_checker)
        col_idx = col_to_index(col_char)

        placed = place_checker(board, col_idx, current_checker)
        if not placed:
            # Column is full, player loses turn
            # But problem states "turn is lost" for full column, no retry
            # Just move on to next player
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
