import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26   # max allowed columns
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4      # number of checkers in a row needed to win

# Checkers symbols for players, index corresponds to player number - 1
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Number of players for this assignment (set to 2 as per submission instructions)
NUM_PLAYERS = 2

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create an empty board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board following the given format with column labels."""
    cols = len(board[0])
    rows = len(board)

    # Print column headers (A, B, C, ...)
    header = "  "
    for c in range(cols):
        header += f"  {chr(ord('A') + c)} "
    print(header)

    # Print the board with row grid and values
    separator = "+" + "---+" * cols
    for r in range(rows):
        print(separator)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(separator)

def valid_column_input(input_str, cols):
    """
    Check if the input is a single uppercase letter within valid column range.
    Returns the column index if valid, else returns None.
    """
    if len(input_str) != 1:
        return None
    c = input_str[0]
    if not ('A' <= c <= chr(ord('A') + cols - 1)):
        return None
    return ord(c) - ord('A')

def place_checker(board, col, checker):
    """
    Place the checker in the chosen column.
    Returns True if checker placed, False if the column is full.
    The checker falls to the lowest available position in the column.
    """
    rows = len(board)
    # Start from bottom row and move upwards to find empty cell
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False

def check_for_win(board, checker):
    """
    Check if the given checker has 4 in a row horizontally, vertically or diagonally.
    Returns True if the player wins, otherwise False.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal check (bottom-left to top-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            # Check this diagonal segment
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal check (top-left to bottom-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def is_board_full(board):
    """Check if all cells in the board are filled with no spaces."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Validate constants
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return
    if COLUMNS > MAX_COLUMNS:
        print(f"Number of columns must be at most {MAX_COLUMNS}.")
        return

    # Create the board
    board = create_board(ROWS, COLUMNS)

    # Select first player randomly
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        player_checker = PLAYER_CHECKERS[current_player_index]
        prompt = f"Player {player_checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(prompt).strip().upper()
            col_index = valid_column_input(user_input, COLUMNS)
            if col_index is None:
                # Invalid input, ask again
                pass
            else:
                # Check if column is full
                if board[0][col_index] != ' ': 
                    # The top cell is occupied, column full lose turn
                    break
                else:
                    # Valid column and not full
                    break

        # If user input invalid or column full (col_index is None or column full, user loses turn)
        if col_index is None:
            # Turn lost - do nothing but print again next round
            clear_screen()
            print_board(board)
            print(f"Invalid move. Player {player_checker} loses this turn.")
            # Switch player for next turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            input("Press Enter to continue...")
            continue
        elif board[0][col_index] != ' ':
            # Column full, lose turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col_index)} is full. Player {player_checker} loses this turn.")
            # Switch player for next turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            input("Press Enter to continue...")
            continue

        # Place checker
        placed = place_checker(board, col_index, player_checker)
        if not placed:
            # Should not happen as we checked for full column above
            clear_screen()
            print_board(board)
            print(f"Could not place checker in column {chr(ord('A') + col_index)}. Turn lost.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            input("Press Enter to continue...")
            continue

        # Check for win
        if check_for_win(board, player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Switch player turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
