import os
import random
import string

# ------------------------- Configuration -------------------------

# Board dimensions (ROWS x COLS). Submission requires 6 x 7.
ROWS = 6
COLS = 7  # Max 26 (A-Z)

# Number of players (2 to 5). Submission requires 2 players.
NUM_PLAYERS = 2

# Player checker symbols in order of assignment.
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# ------------------------- Validation ----------------------------

def validate_constants() -> None:
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough PLAYER_SYMBOLS for NUM_PLAYERS.")
    if not (1 <= ROWS):
        raise ValueError("ROWS must be at least 1.")
    if not (1 <= COLS <= 26):
        raise ValueError("COLS must be between 1 and 26.")
    # A standard Connect 4 requires at least 4x4 to be winnable
    if ROWS < 4 and COLS < 4:
        raise ValueError("Board must be at least 4 cells in one dimension to allow a win.")

# ------------------------- Game Logic ----------------------------

def create_board(rows: int, cols: int) -> list[list[str]]:
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen() -> None:
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')

def column_labels(cols: int) -> list[str]:
    """Return labels A.. for each column."""
    return [string.ascii_uppercase[i] for i in range(cols)]

def print_board(board: list[list[str]]) -> None:
    """Print the game board with column labels and grid."""
    labels = column_labels(len(board[0]))
    # Header
    print("  " + "   ".join(labels))
    # Rows
    horiz = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(horiz)
        row_cells = "| " + " | ".join(board[r]) + " |"
        print(row_cells)
    print(horiz)

def is_valid_column_input(inp: str, cols: int) -> bool:
    """Check if the input is a single letter within A.. for available columns."""
    if len(inp) != 1:
        return False
    if inp not in string.ascii_uppercase[:cols]:
        return False
    return True

def col_index_from_input(inp: str) -> int:
    """Convert a column label (e.g., 'A') to index 0-based."""
    return ord(inp) - ord('A')

def find_next_open_row(board: list[list[str]], col: int) -> int | None:
    """Return the row index where the checker will land in the given column, or None if full."""
    # Start from bottom row upward for gravity
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board: list[list[str]], col: int, symbol: str) -> int | None:
    """Place the checker in the column if possible, return the row index or None if column is full."""
    row = find_next_open_row(board, col)
    if row is None:
        return None
    board[row][col] = symbol
    return row

def count_in_direction(board: list[list[str]], start_r: int, start_c: int, dr: int, dc: int, symbol: str) -> int:
    """Count consecutive symbols from (start_r, start_c) moving (dr, dc) exclusive of the start."""
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board: list[list[str]], row: int, col: int, symbol: str, needed: int = 4) -> bool:
    """Check if placing symbol at (row, col) creates a connect-4 in any direction."""
    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1  # include the placed checker
        total += count_in_direction(board, row, col, dr, dc, symbol)
        total += count_in_direction(board, row, col, -dr, -dc, symbol)
        if total >= needed:
            return True
    return False

def is_board_full(board: list[list[str]]) -> bool:
    """Check if the board is full (no spaces in the top row)."""
    return all(cell != " " for cell in board[0])

# ------------------------- Game Loop -----------------------------

def main() -> None:
    validate_constants()

    rows, cols = ROWS, COLS
    board = create_board(rows, cols)
    labels = column_labels(cols)

    # Assign player symbols
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]}, please enter a column:")

    # Game loop
    while True:
        # Read and validate input (invalid inputs: re-prompt; full column: lose turn)
        while True:
            user_inp = input().strip().upper()
            if is_valid_column_input(user_inp, cols):
                break
            else:
                print(f"Invalid input. Please enter a letter between {labels[0]} and {labels[-1]}:")

        col = col_index_from_input(user_inp)

        placed_row = drop_checker(board, col, players[current_player_idx])
        clear_screen()

        if placed_row is None:
            # Column full: lose turn, board unchanged from last turn, but still show it
            print_board(board)
            print(f"Column {labels[col]} is full. Player {players[current_player_idx]} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            # Successfully placed
            print_board(board)

            # Check for a win
            if check_win(board, placed_row, col, players[current_player_idx], needed=4):
                print(f"Player {players[current_player_idx]} won!")
                break

            # Check for draw
            if is_board_full(board):
                print("It's a draw!")
                break

            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

        # Prompt next player
        print(f"Player {players[current_player_idx]}, please enter a column:")

if __name__ == "__main__":
    main()
