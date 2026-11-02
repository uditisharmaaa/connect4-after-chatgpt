import os
import random
import sys

# Constants (you may change for testing, but submit with these values)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5

# Token order for players (first N tokens are used)
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    # Clear screen for Linux/Unix terminal as required
    os.system('clear')


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Board grid
    line = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(line)
        row_cells = "|".join(f" {board[r][c]} " for c in range(cols))
        print(f"|{row_cells}|")
    print(line)


def get_player_tokens(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    return PLAYER_TOKENS[:num_players]


def get_column_from_input(cols):
    """
    Prompt until input is a valid column letter within bounds.
    Returns zero-based column index.
    """
    while True:
        try:
            user_input = input().strip()
        except EOFError:
            # In case of EOF, exit gracefully
            sys.exit(0)

        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter for the column:")
            continue

        ch = user_input.upper()
        if not ('A' <= ch <= 'Z'):
            print("Invalid input. Please enter a letter (A-Z):")
            continue

        idx = ord(ch) - ord('A')
        if not (0 <= idx < cols):
            print("Column out of range. Please enter a valid column letter:")
            continue

        return idx


def drop_checker(board, col, token):
    """
    Attempt to drop a checker into column col for player token.
    Returns (placed, row_index) where:
      placed = True if checker placed, False if column full
      row_index = the row where checker was placed, or None if not placed
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return True, r
    return False, None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    # Draw if no empty spaces remain
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Validate column limit
    if COLS > 26:
        raise ValueError("Maximum of 26 columns supported.")

    board = create_board(ROWS, COLS)
    tokens = get_player_tokens(NUM_PLAYERS)

    # Random starting player index
    current_idx = random.randrange(len(tokens))

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_token = tokens[current_idx]
        print(f"Player {current_token}, please enter a column:")
        col = get_column_from_input(COLS)

        placed, placed_row = drop_checker(board, col, current_token)
        if not placed:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_token} loses the turn.")
            # Next player
            current_idx = (current_idx + 1) * 1 % len(tokens)
            continue

        # After a valid placement, update display
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % len(tokens)


if __name__ == "__main__":
    main()
