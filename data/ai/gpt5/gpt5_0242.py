import os
import random
import string
import sys

# -------------------------
# Configuration (constants)
# -------------------------
# You can change these constants to test different board sizes and player counts,
# but your final submission should use ROWS=6, COLS=7, NUM_PLAYERS=2.
ROWS = 6
COLS = 7  # Maximum 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]  # In order, first NUM_PLAYERS are used
WIN_LENGTH = 4  # Number in a row needed to win (always 4 as per assignment)

# -------------------------
# Utility / Validation
# -------------------------
def validate_constants():
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if COLS < 1 or COLS > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if ROWS < 1:
        raise ValueError("ROWS must be at least 1.")
    if len(CHECKERS) < NUM_PLAYERS:
        raise ValueError("Not enough checker symbols provided for the number of players.")

# -------------------------
# Board creation and output
# -------------------------
def create_board(rows, cols):
    # Create ROWS x COLS matrix filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Clear the terminal screen (Linux/Unix/Mac)
    os.system('clear')

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with letters A.. for columns
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(list(letters))
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Rows (top to bottom)
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)

def board_to_string(board):
    # Optional helper if needed elsewhere (not used here)
    # Returns a string representation of the current board.
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(list(letters))
    lines = [header]
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        lines.append(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        lines.append("| " + " | ".join(row_cells) + " |")
    lines.append(sep)
    return "\n".join(lines)

# -------------------------
# Game mechanics
# -------------------------
def get_valid_column_input(num_cols):
    # Keep prompting until the user provides a valid uppercase letter within board range
    letters = string.ascii_uppercase[:num_cols]
    prompt = "Please enter a column ({}): ".format(" or ".join(list(letters)))
    while True:
        try:
            raw = input().strip().upper()
        except EOFError:
            # In case of piped input closure, exit gracefully
            print("\nInput closed. Exiting.")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting.")
            sys.exit(0)

        if len(raw) != 1:
            print(f"Invalid input. Enter a single letter between A and {letters[-1]}.")
            print(prompt, end="")
            continue

        if raw not in letters:
            print(f"Invalid column. Enter a letter between A and {letters[-1]}.")
            print(prompt, end="")
            continue

        col_index = ord(raw) - ord('A')
        return col_index

def drop_checker(board, col, checker):
    # Place the checker in the lowest available row in the specified column.
    # Return the row index where the checker was placed; return None if column is full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None

def is_board_full(board):
    # Return True if there is no empty cell on the board
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False
    return True

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    # Count consecutive checkers from start (exclusive) moving in direction (dr, dc)
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_for_win(board, r, c, checker):
    # Check all four directions that can form a line through (r, c):
    # Horizontal (0,1), Vertical (1,0), Diagonal down-right (1,1), Diagonal up-right (-1,1)
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1  # includes the last placed checker at (r, c)
        total += count_in_direction(board, r, c, dr, dc, checker)
        total += count_in_direction(board, r, c, -dr, -dc, checker)
        if total >= WIN_LENGTH:
            return True
    return False

# -------------------------
# Main game loop
# -------------------------
def main():
    validate_constants()

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial render
    print_board(board)
    print(f"Player {players[current_idx]}, please enter a column:")

    game_over = False
    while not game_over:
        # Read and validate input for column letter
        col = get_valid_column_input(COLS)

        # Attempt to drop the checker
        placed_row = drop_checker(board, col, players[current_idx])

        # Print updated board each turn (as per requirement, clear before printing)
        print_board(board)

        if placed_row is None:
            # Column is full: invalid turn and player loses the turn
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {players[current_idx]} loses the turn.")
            # Check draw even if the move was invalid (unlikely but safe)
            if is_board_full(board):
                print("It's a draw!")
                break
            # Next player's turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            print(f"Player {players[current_idx]}, please enter a column:")
            continue

        # After a successful placement, check for a win
        if check_for_win(board, placed_row, col, players[current_idx]):
            print(f"Player {players[current_idx]} won!")
            game_over = True
            break

        # Check for draw (board full)
        if is_board_full(board):
            print("It's a draw!")
            game_over = True
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS
        print(f"Player {players[current_idx]}, please enter a column:")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Exiting.")
