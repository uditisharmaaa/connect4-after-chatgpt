import os
import random
import string
import sys

# ====== Configuration (change these if needed, but submit with these values) ======
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]  # used in order
WIN_LENGTH = 4  # always 4 per assignment

# ====== Validation of configuration ======
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])

def clear_screen():
    # Per assignment, use clear on Unix-like systems
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header = "  " + "   ".join(COL_LABELS[:cols])
    print(header)
    print("+" + "---+" * cols)

    # Board rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)

def is_valid_column_label(label):
    return len(label) == 1 and label in COL_LABELS

def column_index_from_label(label):
    return COL_LABELS.index(label)

def get_player_input(current_player_token):
    # Keep asking until user provides a syntactically valid, in-range column letter.
    # If invalid input, do not lose the turn.
    while True:
        try:
            user_input = input(f"Player {current_player_token}, please enter a column: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        if not is_valid_column_label(user_input):
            print(f"Invalid column. Please enter one of: {', '.join(COL_LABELS[:COLS])}")
            continue
        return column_index_from_label(user_input)

def place_checker(board, col, token):
    # Places token in the lowest empty row in the given column.
    # Returns the (row, col) where placed, or None if the column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None

def check_direction(board, start_r, start_c, delta_r, delta_c, token):
    rows = len(board)
    cols = len(board[0])
    count = 0

    r, c = start_r, start_c
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
        count += 1
        r += delta_r
        c += delta_c

    return count

def check_win_from_cell(board, row, col, token):
    # Count consecutive tokens including (row, col) in both directions for each axis
    # Directions: horizontal (0,1), vertical (1,0), diag1 (1,1), diag2 (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # count in positive direction including current cell
        pos_count = 0
        r, c = row, col
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
            pos_count += 1
            r += dr
            c += dc
        # count in negative direction excluding current cell
        neg_count = 0
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
            neg_count += 1
            r -= dr
            c -= dc

        if pos_count + neg_count >= WIN_LENGTH:
            return True
    return False

def check_win(board, last_move, token):
    if last_move is None:
        return False
    row, col = last_move
    return check_win_from_cell(board, row, col, token)

def is_draw(board):
    # Draw if no spaces left in top row of any column
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)
    current_token = PLAYER_TOKENS[current_player_index]

    # Initial board print before the game starts
    print_board(board)

    while True:
        # Ask for input (validated for syntax and range)
        col = get_player_input(current_token)

        # Attempt to place checker
        move = place_checker(board, col, current_token)

        # Print updated or unchanged board (must clear before printing)
        print_board(board)

        if move is None:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {COL_LABELS[col]} is full. Player {current_token} loses the turn.")
        else:
            # Check for a win
            if check_win(board, move, current_token):
                print(f"Player {current_token} won!")
                break

            # Check for draw
            if is_draw(board):
                print("The game is a draw.")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_token = PLAYER_TOKENS[current_player_index]

if __name__ == "__main__":
    main()
