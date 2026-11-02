import os
import random
import string

# ---------------------
# Constants
# ---------------------
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY = ' '

# ---------------------
# Utility Functions
# ---------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # On Windows use 'cls'

def print_board(board):
    """Prints the current state of the board."""
    # Print column headers (letters)
    header = "  " + "   ".join(string.ascii_uppercase[:COLUMNS])
    print(header)
    print("+" + "---+" * COLUMNS)
    # Print each row
    for row in board:
        line = "| " + " | ".join(row) + " |"
        print(line)
        print("+" + "---+" * COLUMNS)

def create_board():
    """Creates and returns a board initialized with empty spaces."""
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def is_valid_column(col):
    """Checks if the column character input is valid and within bounds."""
    return len(col) == 1 and col.isalpha() and col.upper() in string.ascii_uppercase[:COLUMNS]

def is_column_full(board, col_idx):
    """Checks if a column is already full."""
    return all(row[col_idx] != EMPTY for row in board)

def place_checker(board, col_idx, checker):
    """Places a checker in the lowest empty space in the column. Returns row or None if full."""
    for row_idx in range(ROWS-1, -1, -1):  # Bottom up
        if board[row_idx][col_idx] == EMPTY:
            board[row_idx][col_idx] = checker
            return row_idx
    return None

def board_full(board):
    """Checks if the board is completely full."""
    for row in board:
        if EMPTY in row:
            return False
    return True

def check_win(board, row_idx, col_idx, checker):
    """Checks if placing a checker at (row_idx, col_idx) wins the game."""
    return (check_line(board, row_idx, col_idx, checker, 1, 0) or  # Horizontal
            check_line(board, row_idx, col_idx, checker, 0, 1) or  # Vertical
            check_line(board, row_idx, col_idx, checker, 1, 1) or  # Diagonal down-right
            check_line(board, row_idx, col_idx, checker, 1, -1))   # Diagonal up-right

def check_line(board, row_idx, col_idx, checker, delta_row, delta_col):
    """Helper to check a direction for win."""
    count = 1  # Count includes the current checker.
    # Check one direction
    r, c = row_idx + delta_row, col_idx + delta_col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    # Check the opposite direction
    r, c = row_idx - delta_row, col_idx - delta_col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col
    return count >= 4

def get_player_input(board, current_checker):
    """Prompts and validates player input. Returns valid column index, or None for a lost turn."""
    while True:
        col = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(col):
            print("Invalid input. Please enter a valid column letter (e.g., A-G).")
            continue
        col_idx = ord(col) - ord('A')
        if is_column_full(board, col_idx):
            print("This column is full. You lose your turn!")
            return None
        return col_idx

# ---------------------
# Main Game Loop
# ---------------------

def main():
    # Setup game
    global COLUMNS, ROWS, NUM_PLAYERS
    assert 2 <= NUM_PLAYERS <= 5
    assert 1 <= COLUMNS <= MAX_COLUMNS
    assert 4 <= ROWS

    board = create_board()

    # Map players to checkers
    players = CHECKERS[:NUM_PLAYERS]

    # Select starting player at random
    current = random.randrange(NUM_PLAYERS)

    clear_screen()
    print_board(board)

    while True:
        checker = players[current]
        col_idx = get_player_input(board, checker)
        clear_screen()  # Always clear after the turn
        if col_idx is None:
            print_board(board)
            # Player loses turn if column is full
            current = (current + 1) % NUM_PLAYERS
            continue
        row_idx = place_checker(board, col_idx, checker)
        print_board(board)
        if row_idx is not None:
            if check_win(board, row_idx, col_idx, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        # Move to next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
