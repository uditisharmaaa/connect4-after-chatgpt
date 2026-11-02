import os
import random
import sys

# =============================
# Configuration constants
# =============================
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Choose how many players are in the game (2–5).
NUM_PLAYERS = 2

# Tokens must be at least as many as NUM_PLAYERS.
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# =============================
# Basic validations of constants
# =============================
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if len(PLAYER_TOKENS) < NUM_PLAYERS:
    print("Error: Not enough PLAYER_TOKENS for the number of players.")
    sys.exit(1)

# Use only the first NUM_PLAYERS tokens
PLAYER_TOKENS = PLAYER_TOKENS[:NUM_PLAYERS]


# =============================
# Utility functions
# =============================

def clear_screen():
    """
    Clear the terminal screen using the requested 'clear' command.
    """
    os.system('clear')


def create_board(rows=ROWS, cols=COLS):
    """
    Create an empty board represented as a list of lists.
    Each cell contains ' ' (space) when empty.
    Board indexing: board[row][col], with row 0 at the top.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board to the terminal with column labels at the top,
    and rows from top to bottom.
    """
    # Column labels
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))
    print("+" + "---+" * len(board[0]))
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * len(board[0]))


def col_from_label(label):
    """
    Convert a column label like 'A' to a column index (0-based).
    Returns None if invalid.
    """
    label = label.upper()
    if label in COLUMN_LABELS[:COLS]:
        return ord(label) - ord('A')
    return None


def get_next_open_row(board, col):
    """
    Return the lowest available row index in the given column (dropping from the bottom).
    If the column is full, return None.
    """
    for r in range(len(board) - 1, -1, -1):  # start from bottom row
        if board[r][col] == ' ':
            return r
    return None


def is_valid_move(board, col):
    """
    Check if a move to the given column index is valid (within range and not full).
    """
    if col < 0 or col >= len(board[0]):
        return False
    return board[0][col] == ' '  # top cell empty means column not full


def drop_piece(board, row, col, token):
    """
    Place a token into the board at (row, col).
    """
    board[row][col] = token


def check_direction(board, start_r, start_c, delta_r, delta_c, token):
    """
    Check 4-in-a-row in a specific direction starting from (start_r, start_c)
    moving by (delta_r, delta_c).
    Returns True if 4 in a row is found.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    count = 0

    for _ in range(4):
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r += delta_r
            c += delta_c
        else:
            return False
    return count == 4


def check_win(board, token):
    """
    Check if the specified token has a connect-4 anywhere on the board.
    Directions checked: horizontal, vertical, diagonal down-right, diagonal up-right.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal (→): start columns 0..(cols-4), all rows
    for r in range(rows):
        for c in range(cols - 3):
            if check_direction(board, r, c, 0, 1, token):
                return True

    # Vertical (↓): start rows 0..(rows-4), all columns
    for r in range(rows - 3):
        for c in range(cols):
            if check_direction(board, r, c, 1, 0, token):
                return True

    # Diagonal down-right (↘): start rows 0..(rows-4), cols 0..(cols-4)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if check_direction(board, r, c, 1, 1, token):
                return True

    # Diagonal up-right (↗): start rows 3..(rows-1), cols 0..(cols-4)
    for r in range(3, rows):
        for c in range(cols - 3):
            if check_direction(board, r, c, -1, 1, token):
                return True

    return False


def is_draw(board):
    """
    A draw occurs when the board is full (no spaces in the top row).
    """
    return all(cell != ' ' for cell in board[0])


def prompt_move(current_token):
    """
    Prompt the current player for a column choice.
    Valid input: A-G (case-insensitive).
    Returns the chosen column index, or None if user chose to quit.
    """
    while True:
        user_input = input(f"Player {current_token}, choose a column (A-{COLUMN_LABELS[COLS-1]}) or Q to quit: ").strip()
        if not user_input:
            print("Please enter a column letter.")
            continue

        if user_input.lower() == 'q':
            return None

        col = col_from_label(user_input)
        if col is None:
            print(f"Invalid column. Please enter a letter from A to {COLUMN_LABELS[COLS-1]}.")
            continue

        return col


# =============================
# Main game loop
# =============================

def main():
    board = create_board(ROWS, COLS)

    # Randomly select the starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {', '.join(PLAYER_TOKENS)}")
        print_board(board)

        current_token = PLAYER_TOKENS[current_player_index]

        # Get a valid move
        col = prompt_move(current_token)
        if col is None:
            print("Game aborted by user.")
            break

        # Validate move (column not full)
        if not is_valid_move(board, col):
            print("That column is full or invalid. Press Enter to try again...")
            input()
            continue

        # Find the next open row and drop the piece
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_token)

        # Check for a win
        if check_win(board, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            break

        # Check for a draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! Board is full.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
