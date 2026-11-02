import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6                 # Number of rows (default 6 for submission)
COLS = 7                 # Number of columns (default 7 for submission; max 26)
NUM_PLAYERS = 2          # Number of players (2 to 5 as per assignment)
TOKENS = ['X', 'O', 'V', 'H', 'M']  # Tokens in order for up to 5 players
WIN_LENGTH = 4           # Always 4 in a row to win

# =========================
# Utility functions
# =========================

def clear_screen():
    # Clear terminal screen (Unix/Linux)
    os.system('clear')


def create_board(rows, cols):
    # Initialize board with spaces
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers (A..)
    headers = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(headers)
    # Top border
    print('+' + '---+' * cols)
    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {cell} ' for cell in row_cells) + '|')
        print('+' + '---+' * cols)


def get_valid_column_input(cols, current_token):
    # Prompt user until a syntactically valid column letter is provided (in range)
    while True:
        try:
            user_in = input(f"Player {current_token}, please enter a column: ").strip()
        except EOFError:
            # End gracefully on EOF
            print()
            sys.exit(0)

        if len(user_in) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        ch = user_in.upper()
        if ch < 'A' or ch > 'Z':
            print("Invalid input. Please enter a letter A-Z.")
            continue
        col = ord(ch) - ord('A')
        if not (0 <= col < cols):
            print("Invalid column. Please enter a letter within the board range.")
            continue
        return col


def find_drop_row(board, col):
    # Return the lowest available row index in the column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None


def place_checker(board, col, token):
    # Place token in the given column if space available; return (row, col) or None if column is full
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= WIN_LENGTH:
                    return True
    return False


def check_draw(board):
    # Draw if no spaces left
    for row in board:
        if ' ' in row:
            return False
    return True


def select_players(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    return TOKENS[:num_players]


def game_loop(board, players):
    rows = len(board)
    cols = len(board[0])

    # Randomly select starting player index
    current_idx = random.randrange(len(players))

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        current_token = players[current_idx]

        # Ask for a valid column letter (in board range)
        col = get_valid_column_input(cols, current_token)

        # Attempt to place checker
        drop_pos = place_checker(board, col, current_token)

        # Clear and show updated board regardless (spec: clear screen before printing updated board)
        clear_screen()
        print_board(board)

        if drop_pos is None:
            # Column full: player loses the turn
            print("Column is full. Turn lost.")
        else:
            # Check for win
            if check_win(board, current_token):
                print(f"Player {current_token} won!")
                break
            # Check for draw
            if check_draw(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_idx = (current_idx + 1) % len(players)


def main():
    # Validate COLS limit
    if COLS > 26:
        raise ValueError("Maximum supported columns is 26 (A-Z).")

    # Prepare game
    board = create_board(ROWS, COLS)
    players = select_players(NUM_PLAYERS)

    # Print an initial board preview before starting (as per spec)
    clear_screen()
    print_board(board)

    # Start the game loop
    game_loop(board, players)


if __name__ == "__main__":
    main()
