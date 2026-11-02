import os
import random
import string

# =========================
# Configuration (changeable)
# =========================
ROWS = 6            # Number of rows (default 6)
COLUMNS = 7         # Number of columns (default 7), maximum 26
NUM_PLAYERS = 2     # Number of players (2 to 5)

# Player checkers in order, as specified
CHECKERS = ["X", "O", "V", "H", "M"]

# Win condition (always 4 per assignment)
CONNECT_N = 4

# =========================
# Validation of configuration
# =========================
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= ROWS, "ROWS must be >= 1."
assert 1 <= COLUMNS <= 26, "COLUMNS must be between 1 and 26."
PLAYERS = CHECKERS[:NUM_PLAYERS]

# =========================
# Utility functions
# =========================
def clear_screen():
    # Per assignment, ensure clear on Unix. Also fallback for Windows.
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column letters
    print("  " + "   ".join(labels))
    # Horizontal line
    hline = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(hline)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(hline)

def is_full_column(board, col):
    # If topmost row in col is not empty, column is full
    return board[0][col] != " "

def drop_checker(board, col, checker):
    """
    Drops a checker into the given column.
    Returns the (row, col) position where checker lands, or None if column is full.
    """
    if is_full_column(board, col):
        return None
    rows = len(board)
    # Start from bottom, find first empty
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return (r, col)
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers from (start_r, start_c) moving (dr, dc),
    not including (start_r, start_c).
    """
    rows = len(board)
    cols = len(board[0])
    r = start_r + dr
    c = start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def has_won(board, last_r, last_c, checker):
    """
    Check for CONNECT_N in a row through (last_r, last_c) for the given checker.
    Directions: horizontal, vertical, diagonal1 (/), diagonal2 (\)
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1),  # Diagonal /
    ]
    for dr, dc in directions:
        total = 1  # include last placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, checker)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= CONNECT_N:
            return True
    return False

def is_draw(board):
    # Draw if no empty cell in the top row of any column
    return all(cell != " " for cell in board[0])

def get_valid_column_input(cols, prompt):
    """
    Prompt user until a syntactically valid column letter is given (within board).
    Returns the zero-based column index.
    Invalid inputs (numbers, out of range letters, etc.) will keep prompting.
    """
    labels = column_labels(cols)
    label_set = set(labels)
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        # Accept case-insensitive, but assignment specifies uppercase. We convert to uppercase.
        col_label = user_input.upper()
        if len(col_label) != 1 or col_label not in label_set:
            print(f"Invalid input. Please enter a single letter between {labels[0]} and {labels[-1]}.")
            continue
        return labels.index(col_label)

def main():
    board = create_board(ROWS, COLUMNS)

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)
    current_checker = PLAYERS[current_player_idx]

    # Initial board display
    clear_screen()
    print_board(board)
    print(f"Player {current_checker}, please enter a column:")

    # Game loop
    while True:
        # Get validated column input (within board range)
        col = get_valid_column_input(COLUMNS, "")

        # Attempt to drop the checker
        pos = drop_checker(board, col, current_checker)

        # Clear and print board after attempted move
        clear_screen()
        print_board(board)

        if pos is None:
            # Column full: invalid turn, player loses the turn
            print(f"Column {column_labels(COLUMNS)[col]} is full. Player {current_checker} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            current_checker = PLAYERS[current_player_idx]
            # Prompt next player
            print(f"Player {current_checker}, please enter a column:")
            continue

        # Check for win
        r, c = pos
        if has_won(board, r, c, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        current_checker = PLAYERS[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

if __name__ == "__main__":
    main()
