import os
import random
import string
import sys

# -----------------------------
# Configuration (constants)
# -----------------------------
ROWS = 6            # Number of rows (default 6)
COLS = 7            # Number of columns (default 7)
NUM_PLAYERS = 2     # Number of players (2 to 5)

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
EMPTY_CELL = " "
WIN_LENGTH = 4      # Number of consecutive checkers needed to win
MAX_COLS = 26       # Max supported columns (A-Z)

# -----------------------------
# Validation of configuration
# -----------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS > MAX_COLS:
    print(f"Error: COLS must be at most {MAX_COLS}.")
    sys.exit(1)

# -----------------------------
# Game helpers
# -----------------------------
def clear_screen():
    # Per assignment, use 'clear'
    os.system('clear')


def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Returns list of 'A', 'B', ... up to number of columns
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header row with column letters
    header = "  " + "   ".join(labels)
    print(header)

    # Separator line
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def next_player_index(current, total):
    return (current + 1) % total


def get_players(num_players):
    return PLAYER_SYMBOLS[:num_players]


def get_valid_input(valid_labels):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        # Must be a single uppercase letter that is in valid_labels
        if len(user_input) != 1:
            print("Invalid input. Enter a single column letter (e.g., A, B, C).")
            continue
        if user_input not in valid_labels:
            print(f"Invalid column. Choose one of: {', '.join(valid_labels)}")
            continue
        return user_input


def drop_checker(board, col_index, symbol):
    # Drop from bottom up: find lowest empty row
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = symbol
            return r  # return row placed
    return None  # column is full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    L = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == L:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    # Draw if no empty cells remain
    for row in board:
        if EMPTY_CELL in row:
            return False
    return True


def game_loop():
    board = create_board(ROWS, COLS)
    players = get_players(NUM_PLAYERS)
    labels = column_labels(COLS)

    # Randomly select starting player
    current_player_idx = random.randrange(len(players))

    # Print initial board state before game starts
    print_board(board)
    print(f"Player {players[current_player_idx]}, please enter a column:")

    while True:
        # Get and validate input
        user_col_label = get_valid_input(labels)
        col_index = labels.index(user_col_label)

        # Attempt to drop checker
        placed_row = drop_checker(board, col_index, players[current_player_idx])

        if placed_row is None:
            # Column full: invalid turn, player loses turn
            print_board(board)
            print(f"Column {user_col_label} is full. Player {players[current_player_idx]} loses the turn.")
            current_player_idx = next_player_index(current_player_idx, len(players))
            print(f"Player {players[current_player_idx]}, please enter a column:")
            continue

        # Successful placement: print board and check win/draw
        print_board(board)

        # Check win
        if check_win(board, players[current_player_idx]):
            print(f"Player {players[current_player_idx]} won!")
            return

        # Check draw
        if check_draw(board):
            print("The game is a draw.")
            return

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, len(players))
        print(f"Player {players[current_player_idx]}, please enter a column:")


def main():
    game_loop()


if __name__ == "__main__":
    main()
