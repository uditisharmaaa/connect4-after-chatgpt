import random
import os
import string
import sys

# ==============================
# Configuration (change these as needed for testing)
# ==============================
ROWS = 6                 # Number of rows on the board
COLS = 7                 # Number of columns on the board (max 26)
NUM_PLAYERS = 2          # Number of players (between 2 and 5 inclusive)

# Allowed checker symbols in order (choose first NUM_PLAYERS)
CHECKERS = ["X", "O", "V", "H", "M"]

# ==============================
# Utility functions
# ==============================

def clear_screen():
    """
    Clear the terminal screen (Unix/Linux/Mac).
    """
    os.system('clear')


def validate_settings():
    """
    Validate global constants for proper game setup.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)


def create_board(rows, cols):
    """
    Create a rows x cols Connect 4 board initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column labels and grid lines.
    """
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal line piece
    horiz = "+" + "+".join(["---"] * cols) + "+"

    # Board rows
    for r in range(rows):
        print(horiz)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(horiz)


def col_from_input(user_input, cols):
    """
    Convert user input (letter) into a column index.
    Returns an integer index if valid, or None if invalid.
    """
    if not user_input:
        return None
    ch = user_input.strip().upper()
    if len(ch) != 1:
        return None
    if ch < 'A' or ch >= chr(ord('A') + cols):
        return None
    return ord(ch) - ord('A')


def get_valid_column_input(cols, current_checker):
    """
    Prompt the user for a valid column input.
    Keeps asking until the input is a valid column letter.
    Does not check if the column is full here (that determines losing the turn).
    """
    while True:
        try:
            user_input = input(f"Player {current_checker}, please enter a column: ")
        except EOFError:
            # If input stream ends, gracefully exit
            print("\nInput ended. Exiting game.")
            sys.exit(0)
        col = col_from_input(user_input, cols)
        if col is not None:
            return col
        else:
            print("Invalid input. Please enter a valid column letter.")


def drop_checker(board, col, checker):
    """
    Attempt to drop a checker into the specified column.
    Returns:
      - (True, row_index) if successful, with the row where it landed.
      - (False, None) if the column is full (no move made).
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r
    return False, None


def check_win(board, checker):
    """
    Check if the given checker has four in a row somewhere on the board.
    Checks horizontal, vertical, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0])
    target = 4

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Right
        (1, 0),   # Down
        (1, 1),   # Down-right
        (1, -1),  # Down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    count += 1
                    if count == target:
                        return True
                    rr += dr
                    cc += dc
    return False


def board_full(board):
    """
    Return True if the board has no empty spaces, else False.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# ==============================
# Main game loop
# ==============================

def main():
    validate_settings()

    # Select checkers based on number of players
    players = CHECKERS[:NUM_PLAYERS]

    # Initialize board
    board = create_board(ROWS, COLS)

    # Randomly select the starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]} will start.")

    # Game loop
    while True:
        current_checker = players[current_player_idx]

        # Before taking a turn, check if the game is already a draw
        # (e.g., if board is full due to previous moves or no moves possible).
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Prompt for a valid column input (letter within board).
        col = get_valid_column_input(COLS, current_checker)

        # Try to place the checker; if column is full, the player loses the turn.
        placed, _ = drop_checker(board, col, current_checker)
        if not placed:
            # Turn lost; inform the player
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful placement, clear and print updated board
        clear_screen()
        print_board(board)

        # Check for a win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for a draw after a successful move
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
