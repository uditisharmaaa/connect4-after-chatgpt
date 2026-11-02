import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6              # Number of rows (e.g., 6)
COLS = 7              # Number of columns (e.g., 7) - Max 26 due to letter labels
NUM_PLAYERS = 2       # Number of players (between 2 and 5)

# Checker symbols in order. Use the first NUM_PLAYERS of these.
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

# Number of consecutive checkers needed to win
WIN_LENGTH = 4


# =========================
# Utility / Validation
# =========================
def validate_configuration(rows, cols, num_players):
    """Validate configuration constants and exit if invalid."""
    if not (2 <= num_players <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if cols < 1 or cols > 26:
        print("COLS must be between 1 and 26 to support A-Z labels.")
        sys.exit(1)
    if rows < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)


def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


# =========================
# Board functions
# =========================
def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels and cell grid."""
    rows = len(board)
    cols = len(board[0])

    # Header with column letters A.. up to cols
    header_letters = [string.ascii_uppercase[c] for c in range(cols)]
    print("  " + "   ".join(header_letters))
    # Top border
    print("+" + ("---+" * cols))

    # Each row
    for r in range(rows):
        # Row content
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        # Row border
        print("+" + ("---+" * cols))


# =========================
# Game mechanics
# =========================
def get_players(num_players):
    """Return the list of player tokens for the game."""
    return PLAYER_TOKENS[:num_players]


def column_letter_to_index(letter):
    """Convert a column letter (A..Z) to a 0-based column index."""
    letter = letter.upper()
    if len(letter) != 1 or letter < 'A' or letter > 'Z':
        return None
    return ord(letter) - ord('A')


def get_valid_column_input(cols):
    """
    Prompt until the user enters a valid column letter within range.
    Returns the 0-based column index. Does NOT place a checker.
    Invalid inputs do not cost the turn.
    """
    while True:
        user_in = input().strip()
        if not user_in:
            print("Invalid input. Please enter a column letter (e.g., A).")
            continue
        idx = column_letter_to_index(user_in)
        if idx is None:
            print("Invalid input. Please enter a column letter (e.g., A).")
            continue
        if idx < 0 or idx >= cols:
            print("Invalid column. Please enter a letter between A and {}.".format(string.ascii_uppercase[cols - 1]))
            continue
        return idx


def drop_checker(board, col_idx, token):
    """
    Attempt to drop 'token' into column 'col_idx'.
    Returns (success: bool, row_idx: int or None).
    If the column is full, returns (False, None).
    """
    rows = len(board)
    # Start from bottom-most row to top, find first empty space.
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = token
            return True, r
    return False, None


def check_win(board, token):
    """Check if the given token has a winning sequence on the board."""
    rows = len(board)
    cols = len(board[0])
    k = WIN_LENGTH

    # Directions to check: right, down, diag down-right, diag down-left
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token:
                    count += 1
                    if count == k:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    """Return True if the board is full and no more moves can be played."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False
    return True


# =========================
# Main game loop
# =========================
def play_game(rows, cols, num_players):
    """Run the Connect 4 game."""
    validate_configuration(rows, cols, num_players)
    players = get_players(num_players)
    board = create_board(rows, cols)

    # Randomly select starting player
    current_player_idx = random.randint(0, num_players - 1)

    # Initial board print
    clear_screen()
    print_board(board)
    print("Player {}, please enter a column:".format(players[current_player_idx]))

    while True:
        # Get valid column input (does not cost turn if invalid)
        col_idx = get_valid_column_input(cols)

        # Attempt to drop checker
        success, _ = drop_checker(board, col_idx, players[current_player_idx])

        # Clear screen and print board after the attempt (updated or not)
        clear_screen()
        print_board(board)

        if not success:
            # Column full -> player loses the turn
            col_letter = string.ascii_uppercase[col_idx]
            print("Column {} is full. Turn lost.".format(col_letter))
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % num_players

            # After turn (even if invalid placement), check draw (optional; board unchanged)
            if check_draw(board):
                print("It's a draw!")
                break

            print("Player {}, please enter a column:".format(players[current_player_idx]))
            continue

        # Successful placement: check for win
        if check_win(board, players[current_player_idx]):
            print("Player {} won!".format(players[current_player_idx]))
            break

        # Check draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players
        print("Player {}, please enter a column:".format(players[current_player_idx]))


if __name__ == "__main__":
    # Set up and play the game with configured constants.
    play_game(ROWS, COLS, NUM_PLAYERS)
