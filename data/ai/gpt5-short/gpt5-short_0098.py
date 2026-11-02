# Connect 4 (6x7) for 2–5 players
# - Columns labeled A-G
# - Player tokens: X, O, V, H, M (use first NUM_PLAYERS)
# - Random first player
# - Validates input and column fullness
# - Detects wins and draws
# - Clears screen each turn using os.system('clear')

import os
import random
import sys

# -----------------------
# Configuration constants
# -----------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Available player tokens (max 5). The game will use the first NUM_PLAYERS of these.
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Set number of players for your class demo (between 2 and 5)
NUM_PLAYERS = 2  # change to 3, 4, or 5 as desired


# -----------------------
# Utility / game helpers
# -----------------------

def clear_screen():
    """
    Clear the terminal screen.
    Note: This uses the Unix 'clear' command as requested.
    """
    os.system('clear')


def create_board():
    """
    Create an empty Connect 4 board represented as a 2D list.
    We'll use '.' as the empty cell marker to make the board easy to read.
    """
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board, players, current_idx):
    """
    Print the column labels and the board.
    The top of the board is row 0; we print from top to bottom for readability.
    """
    clear_screen()
    # Display players and indicate whose turn it is
    order = ' -> '.join(players)
    print(f"Players (turn order): {order}")
    print(f"Current player: {players[current_idx]}")
    print()

    # Print column headers (A-G)
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print each row
    for r in range(ROWS):
        print(str(ROWS - r) + ' ' + ' '.join(board[r]))
    print()
    # Small legend
    print("Enter a column letter (A-G) to drop your piece.")


def col_from_label(label):
    """
    Convert a column label (A-G) to a zero-based column index.
    Returns None if invalid.
    """
    label = label.upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None


def is_valid_column(board, col):
    """
    A column is valid if it exists and its top cell is empty.
    """
    if col is None or col < 0 or col >= COLS:
        return False
    return board[0][col] == '.'


def get_next_open_row(board, col):
    """
    Return the lowest available row index in the given column.
    If the column is full, return None.
    """
    for r in range(ROWS - 1, -1, -1):  # start from bottom row
        if board[r][col] == '.':
            return r
    return None


def drop_piece(board, row, col, token):
    """
    Place the player's token in the specified location.
    """
    board[row][col] = token


def check_win(board, token):
    """
    Check if the given token has four in a row:
    - Horizontal
    - Vertical
    - Diagonal (down-right)
    - Diagonal (down-left)
    """
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == token and board[r][c + 1] == token and
                board[r][c + 2] == token and board[r][c + 3] == token):
                return True

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == token and board[r + 1][c] == token and
                board[r + 2][c] == token and board[r + 3][c] == token):
                return True

    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == token and board[r + 1][c + 1] == token and
                board[r + 2][c + 2] == token and board[r + 3][c + 3] == token):
                return True

    # Diagonal down-left
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if (board[r][c] == token and board[r + 1][c - 1] == token and
                board[r + 2][c - 2] == token and board[r + 3][c - 3] == token):
                return True

    return False


def is_draw(board):
    """
    The game is a draw if the top row has no empty cells.
    """
    return all(cell != '.' for cell in board[0])


def get_player_move(board, current_token):
    """
    Prompt the current player for a move, validate input, and return the column index.
    Keeps asking until a valid, non-full column is provided.
    """
    while True:
        choice = input(f"Player {current_token}, choose a column (A-G): ").strip().upper()
        # Basic input validation: must be exactly one of A-G
        if len(choice) != 1 or choice not in COLUMN_LABELS:
            print("Invalid input. Please enter a single letter A-G.")
            continue

        col = col_from_label(choice)
        # Check if the column is not full
        if not is_valid_column(board, col):
            print("That column is full. Choose a different column.")
            continue

        return col


def play_game():
    """
    Main game loop:
    - Set up players and board
    - Randomize starting player
    - Alternate turns until win or draw
    """
    # Validate the configuration
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return
    if NUM_PLAYERS > len(PLAYER_TOKENS):
        print("Error: Not enough PLAYER_TOKENS for the selected NUM_PLAYERS.")
        return

    # Select the tokens for this game and decide a random starting index
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    start_index = random.randrange(NUM_PLAYERS)
    current_idx = start_index

    # Initialize game state
    board = create_board()

    # Game loop
    while True:
        print_board(board, players, current_idx)
        current_token = players[current_idx]

        try:
            col = get_player_move(board, current_token)
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted. Exiting.")
            return

        row = get_next_open_row(board, col)
        # get_next_open_row should always find a row here since we validated, but check anyway.
        if row is None:
            print("Unexpected: column is full. Try again.")
            input("Press Enter to continue...")
            continue

        drop_piece(board, row, col, current_token)

        # Check for a win
        if check_win(board, current_token):
            print_board(board, players, current_idx)
            print(f"Player {current_token} wins! Congratulations!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board, players, current_idx)
            print("It's a draw! No more moves available.")
            break

        # Next player's turn (wrap around)
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        play_game()
    except Exception as e:
        # Catch-all to avoid cryptic crashes in an intro class setting
        print("An unexpected error occurred:", e)
        sys.exit(1)
