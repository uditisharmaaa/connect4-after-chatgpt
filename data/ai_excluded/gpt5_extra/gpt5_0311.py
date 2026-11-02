import os
import random
import sys

# ----------------------------
# Configuration (constants)
# ----------------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]


# ----------------------------
# Board utilities
# ----------------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    os.system('clear')


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    for r in range(rows):
        # Row cells
        line = "|"
        for c in range(cols):
            line += f" {board[r][c]} |"
        print(line)
        # Row separator
        print("+" + ("---+" * cols))


def col_from_input(inp):
    inp = inp.strip().upper()
    if len(inp) != 1:
        return None
    if not ('A' <= inp <= 'Z'):
        return None
    col = ord(inp) - ord('A')
    if 0 <= col < COLS:
        return col
    return None


def find_drop_row(board, col):
    # Return the row index where a checker will land in this column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, token):
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return row


def board_full(board):
    # If any top cell is empty, board not full
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token and count < 4:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= 4:
                    return True
    return False


# ----------------------------
# Game loop
# ----------------------------
def main():
    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        token = PLAYER_TOKENS[current_player]
        # Prompt and input validation loop (reprompt until valid input; not including full column)
        while True:
            user_input = input(f"Player {token}, please enter a column: ").strip()
            col = col_from_input(user_input)
            if col is None:
                print("Invalid input. Please enter a single letter within the board range (e.g., A-G).")
                continue
            break

        placed = False
        # Attempt to place checker
        drop_row = find_drop_row(board, col)
        if drop_row is None:
            # Column full: player loses turn
            msg = f"Column {chr(ord('A') + col)} is full. Player {token} loses the turn."
            # Print updated (unchanged) board with message
            clear_screen()
            print_board(board)
            print(msg)
        else:
            board[drop_row][col] = token
            placed = True
            # Print updated board after placement
            clear_screen()
            print_board(board)

        # Check win only if a checker was placed
        if placed and check_win(board, token):
            print(f"Player {token} won!")
            break

        # Check for draw (board full)
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
