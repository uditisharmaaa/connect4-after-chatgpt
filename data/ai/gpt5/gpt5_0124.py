import os
import random
import string
import sys

# ====== Configuration constants ======
ROWS = 6            # Number of rows (default for submission: 6)
COLS = 7            # Number of columns (default for submission: 7). Max 26.
NUM_PLAYERS = 2     # Number of players (2 to 5). Default for submission: 2.

CHECKER_ORDER = ["X", "O", "V", "H", "M"]  # Order of player tokens
WIN_LENGTH = 4      # Always 4 for this assignment

# ====== Safety checks for configuration ======
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)

# ====== Board utilities ======
def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clear the terminal screen (Unix-like)."""
    os.system('clear')

def col_label(index):
    """Return the column label (A, B, ..., Z) for a 0-based index."""
    return string.ascii_uppercase[index]

def print_board(board):
    """Print the board with column headers as specified."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header = "  " + "   ".join(col_label(c) for c in range(cols))
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        content = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(content)
        print(sep)

def is_board_full(board):
    """Return True if no spaces remain."""
    for row in board:
        if " " in row:
            return False
    return True

# ====== Input handling ======
def get_valid_column_input(cols):
    """
    Prompt user for a column letter.
    Validate: single letter, within A.. corresponding to cols.
    Keep prompting until valid input is provided.
    Returns 0-based column index.
    """
    valid_letters = [col_label(i) for i in range(cols)]
    prompt = "Please enter a column: "
    while True:
        try:
            raw = input(prompt)
        except EOFError:
            print("\nInput closed. Exiting game.")
            sys.exit(0)
        if not raw:
            print(f"Invalid input. Enter one of: {', '.join(valid_letters)}")
            continue
        s = raw.strip().upper()
        if len(s) != 1 or s not in valid_letters:
            print(f"Invalid input. Enter one of: {', '.join(valid_letters)}")
            continue
        return valid_letters.index(s)

# ====== Game mechanics ======
def lowest_empty_row(board, col):
    """Return the lowest (largest index) empty row for the column, or None if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, checker):
    """
    Attempt to place the checker into the given column.
    Returns (row_index, col) on success, or None if the column is full.
    """
    r = lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = checker
    return (r, col)

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers equal to 'checker' starting at (start_r, start_c),
    moving in direction (dr, dc), not including the starting cell.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, last_r, last_c, win_len=WIN_LENGTH):
    """
    Check if placing at (last_r, last_c) resulted in a win.
    Checks horizontal, vertical, and both diagonals.
    """
    checker = board[last_r][last_c]
    if checker == " ":
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        # Count on both sides, including the placed checker
        count = 1
        count += count_in_direction(board, last_r, last_c, dr, dc, checker)
        count += count_in_direction(board, last_r, last_c, -dr, -dc, checker)
        if count >= win_len:
            return True
    return False

# ====== Main game loop ======
def main():
    rows, cols = ROWS, COLS
    players = CHECKER_ORDER[:NUM_PLAYERS]
    board = create_board(rows, cols)

    # Randomly choose first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial screen
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    while True:
        player = players[current_player_index]
        print(f"Player {player},", end=" ")
        col = get_valid_column_input(cols)

        # Attempt to place checker
        move = place_checker(board, col, player)

        if move is None:
            # Column full: move invalid, player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {col_label(col)} is full. Player {player} loses the turn.")
            # Advance to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Continue to next loop iteration
        else:
            last_r, last_c = move
            clear_screen()
            print_board(board)

            # Check for win
            if check_win(board, last_r, last_c, WIN_LENGTH):
                print(f"Player {player} won!")
                break

            # Check for draw
            if is_board_full(board):
                print("It's a draw!")
                break

            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

        # Prompt line formatting similar to example
        if move is not None:
            # Show next prompt message similar to example
            next_player = players[current_player_index]
            print(f"Player {next_player}, please enter a column:")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
