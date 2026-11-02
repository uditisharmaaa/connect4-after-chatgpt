import os
import random

# ---------------------------
# CONSTANTS
# ---------------------------
ROWS = 6                   # Number of rows for the Connect 4 board
COLS = 7                   # Number of columns for the Connect 4 board (max 26)
NUM_PLAYERS = 2            # Number of players (between 2 and 5)
CHECKERS = ["X", "O", "V", "H", "M"] # Checker symbols for up to 5 players
EMPTY = " "                # Symbol for empty spot

COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)] # ['A', 'B', ..., 'G']

# ---------------------------
# Functions
# ---------------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # For Unix/Linux (Use 'cls' for Windows)

def create_board(rows, cols):
    """Creates and returns a 2D board filled with EMPTY symbols."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board in the requested format."""
    # Header with column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_player_input(player_checker):
    """Returns a validated column index chosen by the current player, or None if invalid input."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        col_letter = user_input.upper()
        if col_letter in COLUMN_LABELS:
            return COLUMN_LABELS.index(col_letter)
        else:
            print(f"Column {col_letter} does not exist. Valid columns: {', '.join(COLUMN_LABELS)}")
            continue

def find_lowest_row(board, col):
    """Returns the index of the lowest empty row in the given column, or None if column is full."""
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY:
            return row
    return None

def drop_checker(board, col, checker):
    """
    Places the checker into the given column.
    Returns (row_index, col_index) if placed, or None if column is full.
    """
    row_index = find_lowest_row(board, col)
    if row_index is not None:
        board[row_index][col] = checker
        return (row_index, col)
    return None

def is_winning_move(board, row, col, checker):
    """Checks if placing 'checker' at (row, col) wins the game."""

    def count_in_direction(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Check in all 4 directions (horizontal, vertical, two diagonals)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count checkers in both directions (forward and backward)
        total = 1 + count_in_direction(dr, dc) + count_in_direction(-dr, -dc)
        if total >= 4:
            return True
    return False

def is_board_full(board):
    """Returns True if the board is completely filled."""
    for row in board:
        if EMPTY in row:
            return False
    return True

def switch_player(player_idx, total_players):
    """Returns the index of the next player."""
    return (player_idx + 1) % total_players

def random_first_player(num_players):
    """Returns random starting player index."""
    return random.randint(0, num_players - 1)

# ---------------------------
# Main Game Logic
# ---------------------------

def main():
    # Set up board and players
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    player_idx = random_first_player(NUM_PLAYERS)
    winner = None

    # Show empty board before start
    clear_screen()
    print_board(board)
    print(f"\nPlayer {players[player_idx]} is randomly chosen to start!\n")

    while True:
        # Print board and prompt input
        clear_screen()
        print_board(board)
        current_checker = players[player_idx]

        col = get_player_input(current_checker)

        # Try to drop checker
        placed = drop_checker(board, col, current_checker)
        if placed is None:
            print(f"Column {COLUMN_LABELS[col]} is full. You lose your turn!")
            # Player loses turn
            player_idx = switch_player(player_idx, NUM_PLAYERS)
            input("Press Enter to continue...")
            continue

        row, col = placed

        # Check for win
        if is_winning_move(board, row, col, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        player_idx = switch_player(player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
