import os
import random
import string
import sys

# ------------ Configuration (can be changed for testing) ------------
ROWS = 6
COLS = 7       # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4   # Always 4 as per assignment

# Checkers are chosen in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']
# -------------------------------------------------------------------


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def column_labels(n):
    # Up to 26 columns (A-Z)
    return [string.ascii_uppercase[i] for i in range(n)]


def print_board(board, labels):
    clear_screen()
    # Header
    header = '  ' + '   '.join(labels)
    print(header)
    # Rows
    rows = len(board)
    cols = len(board[0])
    sep_line = '+' + '+'.join(['---'] * cols) + '+'
    for r in range(rows):
        print(sep_line)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print('|' + '|'.join(row_cells) + '|')
    print(sep_line)


def get_valid_column_input(labels):
    valid_set = set(labels)
    while True:
        user_in = input("Player {}, please enter a column: ".format(current_player_checker)).strip().upper()
        if len(user_in) == 1 and user_in in valid_set:
            return labels.index(user_in)
        # Invalid input: reprompt until valid
        print("Invalid input. Please enter one of: {}.".format(', '.join(labels)))


def drop_checker(board, col_idx, checker):
    # Drop into lowest empty position in column; return row index or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def is_winner(board, checker):
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
                while count < WIN_LENGTH and in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= WIN_LENGTH:
                    return True
    return False


def is_draw(board):
    # Draw if no empty spaces remain
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def setup_players(num_players):
    if not (2 <= num_players <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    return CHECKERS[:num_players]


def validate_config():
    if COLS > 26:
        print("COLS must be <= 26.")
        sys.exit(1)
    if ROWS <= 0 or COLS <= 0:
        print("ROWS and COLS must be positive.")
        sys.exit(1)


def main():
    global current_player_checker  # used in prompt function

    validate_config()
    players = setup_players(NUM_PLAYERS)
    labels = column_labels(COLS)
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_idx = random.randrange(len(players))
    current_player_checker = players[current_idx]

    # Initial board print
    print_board(board, labels)

    # Game loop
    while True:
        # Ask for input; validate only letter/within board
        col = get_valid_column_input(labels)

        # Try to drop checker
        row_placed = drop_checker(board, col, current_player_checker)
        if row_placed is None:
            # Column full: turn is invalid and the player loses the turn
            print_board(board, labels)
            # No need to print an extra message; proceed to next player
        else:
            # Successfully placed: print, then check win/draw
            print_board(board, labels)

            if is_winner(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                break

            if is_draw(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_idx = (current_idx + 1) % len(players)
        current_player_checker = players[current_idx]


if __name__ == "__main__":
    main()
