import os
import random
import string

# ===================== CONSTANT VARIABLES ==========================

NUM_ROWS = 6
NUM_COLS = 7       # board is NUM_ROWS x NUM_COLS
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2    # Set to 2 for submission
CHECKER_SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

# ===================== BOARD FUNCTIONS =============================

def create_board(rows, cols):
    """Creates a board initialized with whitespace."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column headers and grid."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    # Print column labels
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

# ===================== GAME CORE FUNCTIONS =========================

def get_valid_column_input(board, cur_player):
    """Prompt player for a valid column letter and return its index."""
    cols = len(board[0])
    valid_cols = string.ascii_uppercase[:cols]
    while True:
        inp = input(f"Player {cur_player}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_cols:
            print("Invalid input. Please enter a column letter shown above that is not full.")
            continue
        col_idx = valid_cols.index(inp)
        if board[0][col_idx] != " ":
            print("Column is full! You lose your turn.")
            return None  # Special case: lose turn if full
        return col_idx

def place_checker(board, col_idx, checker):
    """Places the checker in the given column, returns row index or None if column is full."""
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx
    return None  # Column full (shouldn't reach here due to input validation)

def is_board_full(board):
    """Returns True if the board is completely full."""
    return all(cell != " " for cell in board[0])

# ===================== WIN CHECKING ================================

def check_winner(board, last_row, last_col, checker):
    """Checks if there's a win after last move (optimizes to only check from last checker)."""
    def count_dir(dx, dy):
        count = 0
        x, y = last_row + dx, last_col + dy
        while 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == checker:
            count += 1
            x += dx
            y += dy
        return count
    # Check all 4 directions: vertical, horizontal, 2 diagonals
    directions = [ (1,0), (0,1), (1,1), (1,-1) ]
    for dx, dy in directions:
        total = 1 + count_dir(dx,dy) + count_dir(-dx,-dy)  # center piece + both sides
        if total >= WIN_LEN:
            return True
    return False

# ===================== GAME LOOP ===================================

def main():
    rows = NUM_ROWS
    cols = NUM_COLS
    num_players = NUM_PLAYERS
    if cols > MAX_COLS or cols < 1:
        print(f"Invalid number of columns. Must be between 1 and {MAX_COLS}.")
        return
    if num_players < MIN_PLAYERS or num_players > MAX_PLAYERS:
        print(f"Players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return
    player_symbols = CHECKER_SYMBOLS[:num_players]

    # Initialize board and player order
    board = create_board(rows, cols)
    current_player_idx = random.randint(0, num_players - 1)

    # Initial board print
    print_board(board)
    print(f"\nPlayer {player_symbols[current_player_idx]} starts!\n")

    # Track winner status
    winner = None
    move_count = 0

    while True:
        cur_checker = player_symbols[current_player_idx]
        col_idx = get_valid_column_input(board, cur_checker)
        # If column is full, lose turn
        if col_idx is None:
            current_player_idx = (current_player_idx + 1) % num_players
            print("\nTurn forfeited. Press Enter to continue...")
            input()
            print_board(board)
            continue
        # Place checker
        row_idx = place_checker(board, col_idx, cur_checker)
        print_board(board)
        move_count += 1

        # Check for win
        if check_winner(board, row_idx, col_idx, cur_checker):
            print(f"Player {cur_checker} won!\n")
            break
        # Check draw
        if is_board_full(board):
            print("The game is a draw!\n")
            break
        # Next player
        current_player_idx = (current_player_idx + 1) % num_players

# ========================= MAIN ENTRY ==============================

if __name__ == "__main__":
    main()
