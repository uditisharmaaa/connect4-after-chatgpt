import os
import random
import sys

# Constants
ROWS = 6
COLS = 7

MIN_PLAYERS = 2
MAX_PLAYERS = 5

WIN_LENGTH = 4

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# For clearing the terminal screen
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create and return a board (list of lists) filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board to the terminal with column labels A..Z."""
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    col_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(col_labels)
    line = "+" + "---+" * cols
    # Print each row from top to bottom
    for r in range(rows):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def is_valid_column_input(input_str, cols):
    """Check if input_str is a single uppercase character representing a valid column."""
    if len(input_str) != 1:
        return False
    ch = input_str[0]
    return 'A' <= ch < chr(ord('A') + cols)

def column_full(board, col):
    """Check if the column is full (no empty spaces)."""
    return board[0][col] != " "

def place_checker(board, col, checker):
    """
    Place the checker in the given column.
    The checker falls to the lowest available row in that column.
    Returns (row_index, col) where checker was placed or None if column full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None

def check_win(board, row, col, checker):
    """
    Check if placing checker at (row, col) causes a win.
    Win if 4 in a row horizontally, vertically, or diagonally.
    """
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Include the placed checker

        # Look forward in direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Look backward in opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    """Check if the entire board is full (no empty spaces)."""
    for col in range(len(board[0])):
        if not column_full(board, col):
            return False
    return True

def get_valid_column_input(board, player_checker):
    """Prompt current player to enter a valid column letter."""
    cols = len(board[0])
    while True:
        print(f"Player {player_checker}, please enter a column:")
        user_input = input().strip().upper()
        if not is_valid_column_input(user_input, cols):
            continue  # ask again
        col = ord(user_input) - ord('A')
        if column_full(board, col):
            # Per spec, if column full, player loses turn, no reprompt
            return None
        return col

def main():
    # Set for submission: 2 players, 6 rows, 7 cols
    rows = ROWS
    cols = COLS
    num_players = 2
    checkers = PLAYER_CHECKERS[:num_players]

    board = create_board(rows, cols)

    # Randomly select first player
    current_player_idx = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        player_checker = checkers[current_player_idx]

        col = get_valid_column_input(board, player_checker)

        if col is None:
            # Column full - player loses turn
            # Just advance to next player
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        row_col_pos = place_checker(board, col, player_checker)
        if row_col_pos is None:
            # Should never happen since we check column full before
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        r, c = row_col_pos
        if check_win(board, r, c, player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
