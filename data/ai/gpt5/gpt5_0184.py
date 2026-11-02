import os
import random
import string

# ==========================
# Configuration (constants)
# ==========================
ROWS = 6                # Number of rows on the board
COLS = 7                # Number of columns on the board (max 26)
NUM_PLAYERS = 2         # Number of players (2 to 5)
WIN_LENGTH = 4          # Number of checkers in a row required to win

# Player checkers in order; first NUM_PLAYERS are used
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Safety clamps for constraints
COLS = max(1, min(COLS, 26))
NUM_PLAYERS = max(2, min(NUM_PLAYERS, len(CHECKERS)))


def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board (list of lists) initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column headers and grid lines."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    col_labels = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(col_labels)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep_line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep_line)


def get_valid_column_input(valid_cols_set):
    """
    Prompt the user until they enter a valid column letter.
    Returns the uppercase column letter.
    """
    while True:
        user_input = input().strip()
        if len(user_input) == 1 and user_input.isalpha():
            letter = user_input.upper()
            if letter in valid_cols_set:
                return letter
        print("Invalid input. Please enter a valid column letter:", end=" ")


def drop_checker(board, col_index, checker):
    """
    Attempt to drop a checker into the specified column.
    Returns the row index where the checker lands, or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, checker):
    """Check for a win condition (4 in a row) for the given checker."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    L = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # Horizontal right
        (1, 0),    # Vertical down
        (1, 1),    # Diagonal down-right
        (-1, 1),   # Diagonal up-right
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
                if count >= L:
                    return True
    return False


def board_full(board):
    """Return True if no empty spaces remain on the board."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def main():
    # Initialize game state
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    col_labels = string.ascii_uppercase[:COLS]
    valid_cols_set = set(col_labels)

    # Randomly select the first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Game loop
    last_message = None
    while True:
        clear_screen()
        print_board(board)
        if last_message:
            print(last_message)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:", end=" ")

        # Get a valid column letter
        col_letter = get_valid_column_input(valid_cols_set)
        col_index = ord(col_letter) - ord('A')

        # Attempt to drop the checker
        row_index = drop_checker(board, col_index, current_checker)

        # If column is full, player loses the turn
        if row_index is None:
            last_message = f"Column {col_letter} is full. Player {current_checker} loses the turn."
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for a win after a successful move
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for a draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        last_message = None


if __name__ == "__main__":
    main()
