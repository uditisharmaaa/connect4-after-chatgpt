import os
import random
import string

# --------------- Constants -------------------
ROWS = 6           # Default rows for Connect 4
COLS = 7           # Default columns for Connect 4
NUM_PLAYERS = 2    # Default number of players (between 2 and 5)
WIN_COUNT = 4      # How many checkers in a row needed to win
MAX_COLS = 26      # Maximum number of columns (A-Z)
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = list(string.ascii_uppercase)

# --------------- Board Functions -------------
def create_board(rows, cols):
    """Creates a game board with empty cells."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clears the screen and prints the board in pretty format."""
    os.system('clear')
    cols = len(board[0])
    # Print column headers
    header = '  ' + '   '.join(COLUMN_LABELS[:cols])
    print(header)
    # Print horizontal boundary
    bound = '+' + '---+' * cols
    for row in board:
        print(bound)
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
    print(bound)

# --------------- Utility Functions -----------
def get_available_row(board, col):
    """Return the lowest empty row (from bottom) in the given column, or None if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def is_valid_column(inp, cols):
    """Checks if the input is a valid column letter within the game range."""
    if len(inp) == 1 and inp in COLUMN_LABELS[:cols]:
        return True
    return False

def board_full(board):
    """Checks if the board is completely full."""
    return all(cell != " " for row in board for cell in row)

# --------------- Win Check Functions ---------
def check_win(board, row, col, checker):
    """Checks whether placing 'checker' at (row, col) wins the game."""
    return (
        count_consecutive(board, row, col, 0, 1, checker) + count_consecutive(board, row, col, 0, -1, checker) - 1 >= WIN_COUNT or  # Horizontal
        count_consecutive(board, row, col, 1, 0, checker) + count_consecutive(board, row, col, -1, 0, checker) - 1 >= WIN_COUNT or  # Vertical
        count_consecutive(board, row, col, 1, 1, checker) + count_consecutive(board, row, col, -1, -1, checker) - 1 >= WIN_COUNT or # Diag \
        count_consecutive(board, row, col, 1, -1, checker) + count_consecutive(board, row, col, -1, 1, checker) - 1 >= WIN_COUNT    # Diag /
    )

def count_consecutive(board, row, col, dr, dc, checker):
    """Counts consecutive 'checker' symbols starting from (row, col) in direction (dr, dc)."""
    count = 0
    rows, cols = len(board), len(board[0])
    r, c = row, col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

# --------------- Main Game Loop --------------
def main():
    # Set up board and players
    rows, cols = ROWS, COLS
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]

    board = create_board(rows, cols)

    # Randomly select first player
    curr_player = random.randint(0, num_players - 1)
    print_board(board)
    print(f"Player {checkers[curr_player]} starts!\nPress enter to begin.")
    input()

    winner = None

    while True:
        print_board(board)
        current_checker = checkers[curr_player]
        while True:
            col_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            # Validate input: must be a single, in-range letter
            if not is_valid_column(col_input, cols):
                print("Invalid column. Please enter a valid column letter.")
                continue

            col = COLUMN_LABELS[:cols].index(col_input)
            row = get_available_row(board, col)
            if row is None:
                print("Column is full! You lose your turn.")
                break  # Lose turn if column is full

            # Place the checker
            board[row][col] = current_checker

            # Check for a win
            if check_win(board, row, col, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                return

            # After a valid move, check draw, then move to next player
            if board_full(board):
                print_board(board)
                print("Game is a draw!")
                return

            # Next player turn
            curr_player = (curr_player + 1) % num_players
            break # move completed, go to next player

        # (If the column was full, we already advanced the player)

if __name__ == "__main__":
    main()
