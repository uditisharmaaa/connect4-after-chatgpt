import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Checkers for players in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Number of players enabled for this submission
NUM_PLAYERS = 2

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a rows x cols board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current game board with column headers."""
    clear_screen()
    # Print column headers A..G
    headers = "  "
    for col in range(len(board[0])):
        headers += " " + chr(ord('A') + col) + "  "
    print(headers)

    # Print horizontal separator line with + and -
    line_sep = "+" + "---+" * len(board[0])

    for row in range(len(board)):
        print(line_sep)
        # Print each cell in the row
        row_str = "|"
        for col in range(len(board[0])):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print(line_sep)

def get_valid_column_input(board, player_checker):
    """Ask current player for a valid column input until valid or column full."""
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Validate single character, A-G (dependent on board columns) and not number
        if len(inp) != 1 or not ('A' <= inp <= chr(ord('A') + COLUMNS - 1)):
            # Invalid character
            continue
        
        col_index = ord(inp) - ord('A')

        # Check if column full:
        # top row (0th index) is empty -> means column not full
        if board[0][col_index] != " ":
            # Column full, player loses turn
            # Return None to signal losing turn
            return None
        return col_index

def drop_checker(board, col, checker):
    """
    Place the checker in the given column at the lowest available space.
    Assumes column is not full.
    """
    # Start from bottom row (ROWS-1) and move up to find first empty cell
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

def check_winner(board, checker):
    """
    Checks if the given player/checker has 4 in a row horizontally, vertically or diagonally.
    Returns True if winner, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    connect = 4

    # Horizontal check
    for r in range(rows):
        for c in range(cols - connect + 1):
            if all(board[r][c + i] == checker for i in range(connect)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - connect + 1):
            if all(board[r + i][c] == checker for i in range(connect)):
                return True

    # Diagonal check (bottom-left to top-right)
    for r in range(connect - 1, rows):
        for c in range(cols - connect + 1):
            if all(board[r - i][c + i] == checker for i in range(connect)):
                return True

    # Diagonal check (top-left to bottom-right)
    for r in range(rows - connect + 1):
        for c in range(cols - connect + 1):
            if all(board[r + i][c + i] == checker for i in range(connect)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full with no empty spaces left.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Initialize board and select random starting player
    board = create_board(ROWS, COLUMNS)

    # Players to use based on number of players enabled
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Select random first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]

        col = get_valid_column_input(board, player_checker)

        if col is None:
            # Column full: skip turn, do not place checker
            # Inform player lost turn
            # Wait for player acknowledgement and continue
            print(f"Column is full. Player {player_checker} loses the turn.")
            input("Press Enter to continue...")
            # Change turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        drop_checker(board, col, player_checker)
        print_board(board)

        # Check for win
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
