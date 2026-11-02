import os
import random
import string

# ------------------- Constants -------------------
BOARD_ROWS = 6             # Number of rows (modifiable)
BOARD_COLS = 7             # Number of columns (modifiable, max 26)
NUM_PLAYERS = 2            # Number of players (between 2-5)
WIN_LENGTH = 4             # Number of checkers in a row needed to win
CHECKERS = ["X", "O", "V", "H", "M"]

# Column labels (A, B, ..., max up to Z)
COLUMN_LABELS = list(string.ascii_uppercase[:BOARD_COLS])

# --------------- Board Initialization ------------

def init_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

# -------------- Board Display/Printing -----------
def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board):
    """Prints the board to the screen."""
    clear_screen()
    # Print column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Print top border
    print("+" + "---+" * BOARD_COLS)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * BOARD_COLS)

# -------------- Input and Validation -------------
def get_player_input(player_checker, board):
    """Prompt the current player for a valid column, return column index."""
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Length 1, must be in COLUMN_LABELS
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print(f"Invalid input. Enter one of: {', '.join(COLUMN_LABELS)}")
            continue
        col_index = COLUMN_LABELS.index(col_input)
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full! Unfortunately, you lose this turn...")
            return None  # lose turn if column is full
        return col_index

# ------------- Place Checker Logic ---------------
def place_checker(board, col_index, checker):
    """
    Place a checker in the lowest empty row of the given column.
    Returns the row index where it was placed, or None if column was full.
    """
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return None

# --------------- Win Condition Check -------------
def check_win(board, row, col, checker):
    """
    Check all directions from (row, col) for WIN_LENGTH in a row.
    Returns True if the player with 'checker' wins.
    """
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        count = 1  # include the placed checker
        # check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check if that's enough for a win
        if count >= WIN_LENGTH:
            return True
    return False

# --------------- Draw Condition Check ------------
def check_draw(board):
    """Return True if the board is full (draw), False otherwise."""
    return all(cell != " " for cell in board[0])

# ------------------- Game Loop -------------------
def play_game():
    """Main game loop for Connect 4."""
    board = init_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomly select a starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {players[current_player]} starts first!\n(Press Enter to begin)")
    input()

    while True:
        print_board(board)
        player_checker = players[current_player]
        col_index = get_player_input(player_checker, board)
        # If turn lost due to full column, just rotate to next player
        if col_index is None:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row_index = place_checker(board, col_index, player_checker)

        # Shouldn't happen, since we check for full at input
        if row_index is None:
            print("Unexpected error: Column is full but wasn't detected.")
            continue

        # Check for win
        if check_win(board, row_index, col_index, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# -------------------- Main -----------------------
if __name__ == "__main__":
    play_game()
