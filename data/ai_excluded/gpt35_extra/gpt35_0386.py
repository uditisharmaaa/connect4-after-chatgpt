import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
MAX_COLS = 26  # maximum columns supported
PLAYERS = 2     # number of players between 2 and 5
WIN_COUNT = 4   # number of checkers in a row needed to win

# Checkers for players in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constants
if COLS > MAX_COLS:
    raise ValueError(f"Number of columns cannot exceed {MAX_COLS}.")
if not (2 <= PLAYERS <= 5):
    raise ValueError("Number of players must be between 2 and 5.")
if PLAYERS > len(CHECKERS):
    raise ValueError(f"Number of players cannot exceed {len(CHECKERS)}.")


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Creates a rows x cols board filled with whitespace.
    Board is a list of rows, each row is a list of columns.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the board with column labels A..G and the grid.
    No row labels.
    """
    cols = len(board[0])
    rows = len(board)

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))

    # Print board rows from top to bottom
    for r in range(rows):
        print("+---" * cols + "+")
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * cols + "+")


def get_valid_column_input(player_char, cols, board):
    """
    Prompts the player to enter a column letter.
    Validates input:
    - single uppercase letter A-(A+cols-1)
    - column is not full (if full, player loses turn, return None)
    Returns: column index or None if the column was full.
    Keeps prompting until valid input is entered.
    """
    col_labels = [chr(ord('A') + i) for i in range(cols)]

    while True:
        user_input = input(f"Player {player_char}, please enter a column: ").strip()
        # Input validation: length, uppercase A-Z, valid columns
        if len(user_input) != 1 or user_input not in col_labels:
            print(f"Invalid input. Enter a letter from A to {col_labels[-1]}.")
            continue

        col_index = ord(user_input) - ord('A')

        # Check if column is full (top-most row occupied)
        if board[0][col_index] != " ":
            # Player loses turn; return None to signal this
            print(f"Column {user_input} is full. You lose your turn.")
            return None

        return col_index


def place_checker(board, col, checker):
    """
    Places the checker in the specified column on the lowest empty space.
    Board rows go from 0 (top) to ROWS-1 (bottom).
    Returns the row where the checker was placed.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Should never reach here if column is validated beforehand
    return None


def check_win(board, last_row, last_col, checker):
    """
    Checks whether placing 'checker' at (last_row, last_col) causes a win.
    Checks horizontally, vertically, and both diagonals.
    Returns True if win, else False.
    """
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        """
        Counts how many continuous 'checker' cells are in direction (dr, dc)
        starting from last_row,last_col excluding the starting cell.
        """
        r, c = last_row + dr, last_col + dc
        count = 0
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal (0,1), vertical (1,0),
    # diagonal1 (1,1), diagonal2 (1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        # Count positive and negative directions
        total = 1  # include the last played checker itself
        total += count_direction(dr, dc)
        total += count_direction(-dr, -dc)
        if total >= WIN_COUNT:
            return True
    return False


def check_draw(board):
    """
    Returns True if board is full, else False.
    Board is full if top row has no empty spaces.
    """
    top_row = board[0]
    return all(cell != " " for cell in top_row)


def main():
    # Initialize game state
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    # Randomly select first player index
    current_player_idx = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        current_checker = players[current_player_idx]

        col = get_valid_column_input(current_checker, COLS, board)
        if col is None:
            # Player loses turn if column is full, move to next player
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        row = place_checker(board, col, current_checker)

        clear_screen()
        print_board(board)

        # Check if current player won
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check if game is draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
