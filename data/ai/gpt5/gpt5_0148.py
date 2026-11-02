import os
import random
import string
import sys

# ====== Configuration (adjustable) ======
ROWS = 6                 # Number of rows (e.g., 6)
COLS = 7                 # Number of columns (e.g., 7) - maximum 26
NUM_PLAYERS = 2          # Number of players (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players
WIN_LENGTH = 4           # Length needed to win (always 4 per spec)
# =======================================

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    # Header with column letters
    header_letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(header_letters))
    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def drop_checker(board, col, checker):
    # Drop the checker to the lowest available row in the given column
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column is full

def get_column_input(cols, current_checker):
    valid_letters = [string.ascii_uppercase[i] for i in range(cols)]
    prompt = f"Player {current_checker}, please enter a column: "
    while True:
        user_in = input(prompt).strip()
        # Validate input: must be a single uppercase letter within range
        if len(user_in) == 1 and user_in in valid_letters:
            return valid_letters.index(user_in)
        # Invalid input: prompt again
        print("Invalid input. Please enter an uppercase letter for a valid column.")

def board_full(board):
    # If any top cell is empty, board is not full (or check all cells)
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    L = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < L and in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                    count += 1
                    nr += dr
                    nc += dc
                if count == L:
                    return True
    return False

def validate_configuration():
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if len(CHECKERS) < NUM_PLAYERS:
        print("Error: Not enough checker symbols provided for the number of players.")
        sys.exit(1)

def main():
    validate_configuration()

    # Initialize
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]

        # Get a valid column input (uppercase letter within range)
        col = get_column_input(COLS, current_checker)

        # Try to drop checker
        placed_row = drop_checker(board, col, current_checker)
        if placed_row is None:
            # Column full -> invalid turn; player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful placement, clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
