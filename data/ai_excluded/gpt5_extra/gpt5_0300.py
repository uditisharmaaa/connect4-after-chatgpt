import os
import random
import string
import sys

# -------------------- Configuration (Submission requires these values) --------------------
ROWS = 6            # Number of rows (e.g., 6)
COLS = 7            # Number of columns (e.g., 7) - must be <= 26
NUM_PLAYERS = 2     # Number of players (2 to 5)

# -------------------- Constants --------------------
MAX_COLS = 26
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# -------------------- Utility Functions --------------------
def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))
    # Separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def get_valid_column_input(cols):
    valid_letters = set(string.ascii_uppercase[:cols])
    while True:
        user_input = input("Player, please enter a column: ").strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        # Accept lowercase by converting to uppercase
        letter = user_input.upper()
        if len(letter) != 1 or not letter.isalpha():
            print("Invalid input. Please enter a single letter for the column.")
            continue
        if letter not in valid_letters:
            print(f"Invalid column. Please choose between A and {string.ascii_uppercase[cols-1]}.")
            continue
        return ord(letter) - ord('A')

def place_checker(board, col, symbol):
    """
    Place symbol in the lowest available row in column 'col'.
    Returns (row_index, col_index) if placed, or (None, None) if column full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            board[r][col] = symbol
            return r, col
    return None, None  # Column full

def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count consecutive 'symbol' starting at (start_r, start_c) and moving in (dr, dc).
    Does not include the starting cell in the count.
    """
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(board, r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, last_r, last_c, symbol):
    """
    Check if placing 'symbol' at (last_r, last_c) results in a win (4 in a row).
    """
    if last_r is None or last_c is None:
        return False

    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # include the last placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY_CELL:
                return False
    return True

def next_player_index(current, total):
    return (current + 1) % total

def validate_settings():
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > MAX_COLS:
        print(f"Error: COLS must be between 1 and {MAX_COLS}.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)

# -------------------- Game Loop --------------------
def main():
    validate_settings()
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    clear_screen()
    print_board(board)

    winner = None
    while True:
        # Prompt message with current player symbol
        print(f"Player {symbols[current_player]}, please enter a column:")
        col = get_valid_column_input(COLS)

        # Attempt to place checker
        r, c = place_checker(board, col, symbols[current_player])

        if r is None:
            # Column full: player loses the turn
            clear_screen()
            print_board(board)
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {symbols[current_player]} loses the turn.")
            current_player = next_player_index(current_player, NUM_PLAYERS)
            continue

        # Successful placement: update display
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, r, c, symbols[current_player]):
            winner = symbols[current_player]
            print(f"Player {winner} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player_index(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    main()
