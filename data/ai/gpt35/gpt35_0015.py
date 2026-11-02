import os
import random

# Constants
NUM_ROWS = 6      # Board rows
NUM_COLUMNS = 7   # Board columns (max 26)
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2   # Set to 2 for submission

CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

WIN_COUNT = 4     # Need 4 in a row to win

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    """Create board initialized with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board as per example output."""
    clear_screen()
    # Print column headers A..G (or dynamic)
    header = "  "
    for col_idx in range(len(board[0])):
        header += f" {chr(ord('A') + col_idx)}  "
    print(header)
    
    # Print horizontal separator and rows
    sep_line = "+" + "---+" * len(board[0])
    for row in range(len(board)):
        print(sep_line)
        # Print each cell with vertical bars
        row_str = "|"
        for col in range(len(board[0])):
            row_str += f" {board[row][col]} |"
        print(row_str)
    print(sep_line)

def is_valid_column_input(col_input, max_col):
    """Check if input is a single uppercase character within board columns."""
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col = ord(col_input.upper()) - ord('A')
    return 0 <= col < max_col

def get_column_index(col_input):
    """Convert column letter to board index."""
    return ord(col_input.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place checker in the lowest empty position in the column.
    Return True if placed, False if column full.
    """
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False  # column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_is_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Prepare variables
    rows = NUM_ROWS
    cols = NUM_COLUMNS
    players = NUM_PLAYERS
    checkers = CHECKERS[:players]

    board = create_board(rows, cols)

    # Random starting player index
    current_player_idx = random.randint(0, players - 1)

    while True:
        print_board(board)
        current_checker = checkers[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        
        # Get valid input with validation loop
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column_input(user_input, cols):
                # Invalid input format or out of range
                continue
            col_idx = get_column_index(user_input)

            # Check column full
            if board[0][col_idx] != " ":
                # Column is full: turn is lost
                break
            else:
                # Valid move possible
                placed = place_checker(board, col_idx, current_checker)
                if placed:
                    break
                else:
                    # Should not reach here because top cell is empty check above
                    break
        
        # If column full (top cell occupied), player loses turn -> no placement
        # Otherwise, we placed checker and must check win/draw

        # Check for win (only if we placed checker successfully)
        if board[0][col_idx] != " ":
            # Means placed (except when column full and turn lost)
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

        # Check for draw
        if board_is_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player turn only if the turn was not lost due to full column input
        if board[0][col_idx] != " ":
            current_player_idx = (current_player_idx + 1) % players
        else:
            # Turn is lost, skipping player rotation
            current_player_idx = (current_player_idx + 1) % players

if __name__ == "__main__":
    main()
