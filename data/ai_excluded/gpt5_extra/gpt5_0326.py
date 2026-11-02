import os
import random
import string

# =========================
# Configuration (constants)
# =========================
ROWS = 6                # Number of rows (default submission: 6)
COLS = 7                # Number of columns (default submission: 7, max 26)
NUM_PLAYERS = 2         # Number of players (2 to 5)
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Tokens in order

WIN_LENGTH = 4          # Always 4 in a row to win

# Safety checks for constraints
COLS = max(1, min(COLS, 26))
NUM_PLAYERS = max(2, min(NUM_PLAYERS, len(PLAYER_TOKENS)))

# =========================
# Utility functions
# =========================

def clear_screen():
    # Clear the terminal screen (Linux/Unix as per instructions)
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels (A, B, C, ...)
    labels = [string.ascii_uppercase[i] for i in range(cols)]

    # Header with letters
    print('  ' + '   '.join(labels))

    # Build horizontal separator for a row: +---+---+...+
    sep = '+' + '+'.join(['---'] * cols) + '+'

    # Print each row
    for r in range(rows):
        print(sep)
        # Build row content like |   | X |   | ...
        row_cells = []
        for c in range(cols):
            row_cells.append(f' {board[r][c]} ')
        print('|' + '|'.join(row_cells) + '|')
    print(sep)

def get_column_index_from_input(user_input, max_cols):
    """
    Convert a single-letter input to a column index. Returns None if invalid.
    """
    if not user_input or len(user_input) != 1:
        return None
    ch = user_input.upper()
    if ch < 'A' or ch > 'Z':
        return None
    idx = ord(ch) - ord('A')
    if 0 <= idx < max_cols:
        return idx
    return None

def find_drop_row(board, col):
    """
    Return the row index where a piece will land if dropped in column 'col'.
    If the column is full, return None.
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def check_win(board, token):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    n = WIN_LENGTH

    # Directions: (dr, dc) Right, Down, Down-Right, Down-Left
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                # Check if a line of length n fits from (r, c)
                end_r = r + (n - 1) * dr
                end_c = c + (n - 1) * dc
                if not (0 <= end_r < rows and 0 <= end_c < cols):
                    continue
                won = True
                for k in range(n):
                    rr = r + k * dr
                    cc = c + k * dc
                    if board[rr][cc] != token:
                        won = False
                        break
                if won:
                    return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# =========================
# Main game loop
# =========================

def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_token = players[current_player_index]
        # Prompt and validate input
        while True:
            user_in = input(f"Player {current_token}, please enter a column: ").strip()
            col = get_column_index_from_input(user_in, COLS)
            if col is None:
                print("Invalid input. Please enter a letter within the board (e.g., A, B, C...).")
                continue
            break

        # Attempt to place checker
        row_to_place = find_drop_row(board, col)
        if row_to_place is None:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {string.ascii_uppercase[col]} is full. Turn lost.")
            # Advance to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Print updated (unchanged) board
            clear_screen()
            print_board(board)
            continue

        # Place checker
        board[row_to_place][col] = current_token

        # After move: clear and print board
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
