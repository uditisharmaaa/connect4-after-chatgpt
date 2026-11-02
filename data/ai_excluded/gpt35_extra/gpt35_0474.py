import os
import random

# Constants for the game configuration
ROWS = 6       # Number of rows in the board
COLUMNS = 7    # Number of columns in the board (max 26)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)

# Players' checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row needed to win
WIN_LENGTH = 4


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, columns):
    """Create initial empty board filled with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """
    Print the current game board with column labels (A, B, ...) and grid lines.
    No row labels.
    """
    clear_screen()
    columns = len(board[0])

    # Print column headers
    header = "  "
    for c in range(columns):
        header += f"  {chr(ord('A') + c)} "
    print(header)

    # Print top border
    print("+" + "---+" * columns)

    # Print rows from top to bottom
    for row in board:
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
        print("+" + "---+" * columns)


def get_valid_column_input(current_player_checker, board):
    """
    Ask the player for a column letter input and validate it.
    Keep asking until valid or return None if column is full (lose turn).
    """
    columns = len(board[0])
    valid_letters = [chr(ord('A') + i) for i in range(columns)]
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ")
        user_input = user_input.strip().upper()

        # Validate length and character
        if len(user_input) != 1:
            print(f"Invalid input '{user_input}'. Please enter a single column letter.")
            continue
        if user_input not in valid_letters:
            print(f"Invalid column '{user_input}'. Please enter a letter from A to {chr(ord('A') + columns - 1)}.")
            continue

        col_index = ord(user_input) - ord('A')

        # Check if column is full (top row filled)
        if board[0][col_index] != " ":
            # Turn lost if column full
            print(f"Column {user_input} is full. Turn lost.")
            return None

        return col_index


def place_checker(board, col_index, checker):
    """
    Place the checker in the lowest empty spot in the specified column.
    Assumes the column is not full.
    """
    rows = len(board)
    # Start from bottom row to top
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index  # Return position where checker was placed


def check_win(board, row, col, checker):
    """
    Check if placing a checker at (row, col) causes a win.
    Win means 4 in a row horizontally, vertically or diagonally.
    """
    rows, columns = len(board), len(board[0])

    def count_direction(dr, dc):
        """Count consecutive checkers of the player in one direction."""
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions to check: horizontal, vertical, two diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        # Count checkers in both directions
        total = 1  # Count the placed checker itself
        total += count_direction(dr, dc)
        total += count_direction(-dr, -dc)
        if total >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    """Check if board is full (no spaces left in top row)."""
    return all(cell != " " for cell in board[0])


def main():
    # Validate constants (just sanity)
    if COLUMNS > 26 or COLUMNS < 1:
        print("Columns must be between 1 and 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    # Select players' checkers based on number of players
    players = CHECKERS[:NUM_PLAYERS]

    # Create the game board
    board = create_board(ROWS, COLUMNS)

    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]

        col_index = get_valid_column_input(current_checker, board)

        if col_index is None:
            # Turn lost due to full column
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place checker
        row, col = place_checker(board, col_index, current_checker)

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
