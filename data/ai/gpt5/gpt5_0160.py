import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
ROWS = 6            # number of rows (default: 6)
COLS = 7            # number of columns (default: 7) - max 26
NUM_PLAYERS = 2     # number of players (2 to 5)

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # available checkers in order


# =========================
# Utility and Game Functions
# =========================
def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    # Create a 2D board filled with single space " "
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column labels (A..)
    labels = list(string.ascii_uppercase[:cols])

    # Header with column letters
    print('  ' + '   '.join(labels))
    # Top border
    print('+' + ('---+' * cols))

    # Rows content (top to bottom)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {ch} ' for ch in row_cells) + '|')
        print('+' + ('---+' * cols))


def is_board_full(board):
    # Board is full if no cell contains a space
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def drop_checker(board, col, checker):
    """
    Attempt to drop 'checker' into column 'col' (0-based).
    Returns True if successful, False if the column is full.
    """
    rows = len(board)
    # Place from bottom to top
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False  # column is full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_winner(board, checker):
    """
    Check whether 'checker' has 4 in a row in any direction.
    """
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
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False


def get_valid_column_input(cols):
    """
    Prompt until user provides a valid column letter (A.. up to cols).
    Returns 0-based column index.
    Invalid inputs are reprompted and the turn is NOT lost.
    """
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        s = input().strip()
        if len(s) != 1:
            print(f"Invalid input. Enter a single letter between A and {valid_letters[-1]}:")
            continue
        ch = s.upper()
        if ch not in valid_letters:
            print(f"Invalid column. Enter a letter between A and {valid_letters[-1]}:")
            continue
        return ord(ch) - ord('A')


def setup():
    # Enforce constraints
    cols = max(1, min(COLS, 26))
    rows = max(1, ROWS)
    num_players = max(2, min(NUM_PLAYERS, 5))

    # Select player tokens in order
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)
    return board, players


def main():
    board, players = setup()
    rows, cols = len(board), len(board[0])

    # Randomly pick starting player
    current = random.randrange(len(players))

    # Initial screen
    clear_screen()
    print_board(board)
    print(f"Player {players[current]}, please enter a column:")

    while True:
        # Read and validate column letter input
        col = get_valid_column_input(cols)

        # Try to drop checker; if full, player loses the turn
        placed = drop_checker(board, col, players[current])
        if not placed:
            # Losing turn due to full column
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {players[current]} loses the turn.")
            # Check for draw (all columns full)
            if is_board_full(board):
                print("It's a draw!")
                return
            # Next player
            current = (current + 1) % len(players)
            print(f"Player {players[current]}, please enter a column:")
            continue

        # Move placed: check for win
        clear_screen()
        print_board(board)

        if check_winner(board, players[current]):
            print(f"Player {players[current]} won!")
            return

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return

        # Next player's turn
        current = (current + 1) % len(players)
        print(f"Player {players[current]}, please enter a column:")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
