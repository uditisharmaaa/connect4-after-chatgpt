import os
import random
import string

# ------------------------------
# CONSTANTS
# ------------------------------
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2  # Must be between 2 and 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
EMPTY_CELL = " "

# ------------------------------
# GAME FUNCTIONS
# ------------------------------

def clear_screen():
    # Clear the terminal screen (use 'clear' for Unix/Linux, 'cls' for Windows)
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows=ROWS, cols=COLS):
    """Create an empty game board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Display the formatted board to the terminal."""
    cols = len(board[0])
    rows = len(board)
    # Print column headers A, B, C, ...
    print("  " + "   ".join(string.ascii_uppercase[:cols]))
    print("+" + "---+" * cols)
    for r in range(rows):
        row_str = "| " + " | ".join(board[r]) + " |"
        print(row_str)
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """Return a list of column indices that are not full."""
    cols = len(board[0])
    rows = len(board)
    valid = [col for col in range(cols) if board[0][col] == EMPTY_CELL]
    return valid

def column_letter_to_index(letter):
    """Convert a column letter (A, B, ...) to its 0-based index."""
    letter = letter.upper()
    if letter in string.ascii_uppercase:
        idx = ord(letter) - ord('A')
        return idx
    return -1

def get_lowest_empty_row(board, col):
    """Return the row index at which to drop the checker in specified column."""
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def is_board_full(board):
    """Check if the entire board is full."""
    return all(cell != EMPTY_CELL for cell in board[0])

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, checker):
    """Check for 4 in a row in all directions for the given checker."""
    cols = len(board[0])
    rows = len(board)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Directions: (dr, dc)
            directions = [ (0,1), (1,0), (1,1), (1,-1)]
            for dr, dc in directions:
                win = True
                for n in range(1, 4):
                    rr, cc = r + n*dr, c + n*dc
                    if not in_bounds(rr, cc, rows, cols) or board[rr][cc] != checker:
                        win = False
                        break
                if win:
                    return True
    return False

def get_player_input(valid_cols, cols):
    """Prompt user to enter a valid column letter and return the column index."""
    while True:
        move = input("Please enter a column: ").strip().upper()
        if len(move) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        idx = column_letter_to_index(move)
        if idx < 0 or idx >= cols:
            print("Invalid column. Please enter a letter between A and {}.".format(string.ascii_uppercase[cols-1]))
            continue
        if idx not in valid_cols:
            print("That column is full. Please choose another.")
            continue
        return idx

def main():
    # Sanity checks
    assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
    assert 4 <= ROWS
    assert 4 <= COLS <= MAX_COLS

    # Select checkers for players
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    player_names = ["Player " + checker for checker in player_checkers]
    player_count = NUM_PLAYERS

    # Create & initialize the board
    board = create_board(ROWS, COLS)
    first_player = random.randrange(player_count)
    current_player = first_player
    turn = 0

    # Print initial empty board
    clear_screen()
    print_board(board)
    print("{} ({}) starts!".format(player_names[current_player], player_checkers[current_player]))

    # Game loop
    while True:
        # Current player's turn
        checker = player_checkers[current_player]
        display_player = player_names[current_player]
        print(f"{display_player} ({checker}), it's your turn.")
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("Board is full. It's a draw!")
            break
        col = get_player_input(valid_cols, COLS)
        row = get_lowest_empty_row(board, col)
        if row is None:
            # Shouldn't happen due to valid_cols
            print(f"Column {string.ascii_uppercase[col]} is full! Skipping turn...")
        else:
            board[row][col] = checker

        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, checker):
            print(f"{display_player} ({checker}) won!")
            break

        # Check draw
        if is_board_full(board):
            print("Board is full. It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % player_count

if __name__ == "__main__":
    main()
