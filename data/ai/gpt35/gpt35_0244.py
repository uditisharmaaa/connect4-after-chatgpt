import os
import random
import sys

# Constants - for submission, board is 6 rows x 7 cols and 2 players
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players, use first n for PLAYERS_COUNT
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Creates a rows x cols board initialized with ' ' (space)."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column labels A .. """
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(labels)
    line = "+" + "---+" * cols
    for r in range(rows):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def valid_column_input(s, max_col):
    """Validate if input s is a valid column letter A.."""
    if len(s) != 1:
        return False
    c = s[0]
    if not ('A' <= c <= chr(ord('A') + max_col - 1)):
        return False
    return True

def column_to_index(c):
    """Convert column letter (A..) to zero-based column index."""
    return ord(c) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in column if possible.
    The checker falls down to the lowest empty row.
    Returns True if placed, False if the column is full.
    """
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True, row, col
    # column full
    return False, -1, -1

def check_direction(board, start_row, start_col, dr, dc, checker):
    """
    Count how many checkers in a continuous line of same checker 
    starting from (start_row, start_col) towards direction (dr, dc).
    Counts the starting cell too.
    """
    count = 0
    r, c = start_row, start_col
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, checker):
    """
    Check if placing checker at (row, col) forms 4 in a row 
    horizontally, vertically, or diagonally.
    """

    # Directions to check: horizontal, vertical, diag1 / diag2
    # For each direction, check line length by counting in both positive and negative directions
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count_pos = check_direction(board, row, col, dr, dc, checker) - 1
        count_neg = check_direction(board, row, col, -dr, -dc, checker) - 1
        total = 1 + count_pos + count_neg
        if total >= WIN_COUNT:
            return True
    return False

def board_full(board):
    """Return True if the board has no empty cells."""
    return all(cell != " " for row in board for cell in row)

def get_player_input(board, current_checker):
    cols = len(board[0])
    while True:
        s = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if not valid_column_input(s, cols):
            # invalid input (including wrong length, invalid char)
            continue
        col = column_to_index(s)
        # check if column full
        if board[0][col] != " ":
            # column full, player loses turn -- handled separately
            return col, False
        return col, True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS_COUNT]

    # Random first player
    current_player_index = random.randint(0, PLAYERS_COUNT - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        col, can_place = get_player_input(board, current_checker)

        if not can_place:
            # Column full: player loses turn, move to next player
            current_player_index = (current_player_index + 1) % PLAYERS_COUNT
            continue

        placed, row, col = place_checker(board, col, current_checker)
        # placed should always be True here as we checked above

        print_board(board)

        # Check win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS_COUNT


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
