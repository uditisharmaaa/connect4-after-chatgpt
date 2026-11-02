import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players as per assignment

# Validate constants for safety
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
assert COLS <= 26, "Maximum number of columns is 26"

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create an empty board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    clear_screen()
    # Print column headers A..G (or more if larger board)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    header = '  ' + '   '.join(col_labels)
    print(header)

    # Print each row with horizontal separators
    row_separator = '+' + ('---+' * len(board[0]))
    for r in range(len(board)):
        print(row_separator)
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
    print(row_separator)

def choose_first_player(num_players):
    """Randomly select the index of the first player."""
    return random.randint(0, num_players - 1)

def input_column(current_player, board):
    """Prompt the current player for a valid column input.
    Returns the 0-based column index or None if column is full (skipping turn).
    """
    valid_cols = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        prompt = f"Player {CHECKERS[current_player]}, please enter a column: "
        inp = input(prompt).strip().upper()
        if len(inp) != 1 or inp not in valid_cols:
            # Invalid input
            continue
        col = ord(inp) - ord('A')

        # Check if column is full
        if board[0][col] != ' ':
            # Column full, player loses turn
            return None
        return col

def place_checker(board, col, checker):
    """Place a checker in the indicated column at the lowest free spot."""
    # Start from bottom row upwards
    for r in reversed(range(len(board))):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col  # Return position where checker placed
    # Should never be reached if checked before for full column
    return None

def check_win(board, checker, row, col):
    """Check if placing checker at (row, col) caused a win."""

    def count_direction(dr, dc):
        """Count contiguous checkers in one direction."""
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        # Count checkers in positive and negative direction
        total = 1  # Include current checker
        total += count_direction(dr, dc)
        total += count_direction(-dr, -dc)
        if total >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    """Return True if the board is full and no moves left."""
    # If any cell in top row is empty, game is not draw yet
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    current_player = choose_first_player(NUM_PLAYERS)
    print_board(board)

    while True:
        col = input_column(current_player, board)

        if col is None:
            # Column full, player loses turn without placing checker
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue

        row, _ = place_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player], row, col):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
