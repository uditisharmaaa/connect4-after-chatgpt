import os
import random
import string
import sys

# Constants (adjustable; submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4  # Always 4 to win per spec
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Header with column labels
    header = "  " + "   ".join(COL_LABELS)
    print(header)
    # Top border and rows
    border = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(border)
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(border)


def get_column_input(player_marker):
    while True:
        user_in = input(f"Player {player_marker}, please enter a column: ").strip()
        if len(user_in) != 1 or not user_in.isalpha():
            continue
        ch = user_in.upper()
        if ch in COL_LABELS:
            return COL_LABELS.index(ch)
        # else keep prompting


def place_checker(board, col, marker):
    # Place from bottom up; return (row, col) if placed, else None if column full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = marker
            return (r, col)
    return None


def count_in_direction(board, start_r, start_c, dr, dc, marker):
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == marker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, marker):
    # If no last move provided, cannot determine win
    if last_r is None or last_c is None:
        return False
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        count = 1  # include last placed
        count += count_in_direction(board, last_r, last_c, dr, dc, marker)
        count += count_in_direction(board, last_r, last_c, -dr, -dc, marker)
        if count >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no empty spaces left anywhere
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    # Print initial empty board before any move
    print_board(board)

    last_move = (None, None)
    while True:
        player_marker = PLAYERS[current_player_index]
        # Prompt for input
        col = get_column_input(player_marker)

        # Attempt to place checker
        placed_pos = place_checker(board, col, player_marker)

        # After attempting the move, print the updated board
        print_board(board)

        if placed_pos is None:
            # Column full: turn is invalid and the player loses the turn
            # No additional prompt this turn
            pass
        else:
            r, c = placed_pos
            last_move = (r, c)
            # Check for win
            if check_win(board, r, c, player_marker):
                print(f"Player {player_marker} won!")
                break
            # Check for draw
            if is_draw(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over


if __name__ == "__main__":
    main()
