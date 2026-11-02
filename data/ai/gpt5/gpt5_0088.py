import os
import random
import sys

# Configuration constants
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    # Top border
    horizontal = "+" + ("---+" * cols)
    for r in range(rows):
        print(horizontal)
        row_cells = "|"
        for c in range(cols):
            row_cells += f" {board[r][c]} |"
        print(row_cells)
    print(horizontal)

def find_lowest_empty_row(board, col):
    # Returns the index of the lowest empty row in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_winner(board, symbol):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < 4 and in_bounds(nr, nc, rows, cols) and board[nr][nc] == symbol:
                    count += 1
                    nr += dr
                    nc += dc
                if count == 4:
                    return True
    return False

def get_valid_column_input(cols, current_symbol):
    while True:
        try:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip()
        except EOFError:
            # If input stream closes, exit gracefully
            print()
            sys.exit(0)

        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue

        ch = user_input.upper()
        if not ('A' <= ch <= 'Z'):
            print("Invalid input. Please enter a letter.")
            continue

        col_index = ord(ch) - ord('A')
        if not (0 <= col_index < cols):
            print("Invalid input. Column out of range.")
            continue

        return col_index, ch

def main():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        # Display whose turn it is (as in example, prompt shows player)
        current_symbol = symbols[current_player_idx]

        # Get and validate user input (column letter)
        col_index, col_letter = get_valid_column_input(COLS, current_symbol)

        # Place checker or lose turn if column is full
        target_row = find_lowest_empty_row(board, col_index)
        if target_row is None:
            # Column full -> turn lost
            print(f"Column {col_letter} is full. Turn lost.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[target_row][col_index] = current_symbol

        # Check for win
        if check_winner(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
