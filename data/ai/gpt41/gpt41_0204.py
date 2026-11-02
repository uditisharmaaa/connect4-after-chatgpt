import os
import random
import string

# ==== CONSTANTS ====
NUM_ROWS = 6                # Board rows
NUM_COLS = 7                # Board columns
PLAYERS = 2                 # Number of players (between 2 and 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Symbols for each player

# ==== FUNCTIONS ====

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # or 'cls' for Windows

def create_board(rows, cols):
    """Initializes board as a 2D list filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board in Connect 4 style with column headers."""
    cols = len(board[0])
    # Column headers (A, B, C, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Print top border
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """Returns a set of valid column letters where at least one cell is empty."""
    cols = len(board[0])
    valid_cols = []
    for col in range(cols):
        if board[0][col] == ' ':  # If top cell is empty, column is not full
            valid_cols.append(string.ascii_uppercase[col])
    return set(valid_cols)

def get_player_input(valid_cols, player_char):
    """Prompts the player for input, validates, and returns the column index or None (if invalid)."""
    while True:
        choice = input(f"Player {player_char}, please enter a column: ").strip().upper()
        # Input must be one letter, must be a valid column
        if len(choice) == 1 and choice in valid_cols:
            return string.ascii_uppercase.index(choice)
        else:
            print("Invalid input. Please enter a valid column letter from:", ' '.join(sorted(valid_cols)))

def place_checker(board, col, checker):
    """
    Places the checker of current player in the specified column (if not full).
    Modifies the board in-place. Returns True if succeeded, False if column is full.
    """
    for row in reversed(board):  # Start from bottom row
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the given player has 4 in a row: horizontal, vertical, diagonal."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            # Skip non-matching cell
            if board[r][c] != checker:
                continue
            # Check right
            if c + 3 < cols and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Check down
            if r + 3 < rows and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Check down-right diagonal
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Check down-left diagonal
            if r + 3 < rows and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Returns True if the board is full (no empty spaces)."""
    for cell in board[0]:  # If top row has no spaces, board is full
        if cell == ' ':
            return False
    return True

def main():
    # Set up board and player order
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = CHECKERS[:PLAYERS]
    starting_player = random.randint(0, PLAYERS - 1)
    player_indices = list(range(PLAYERS))
    # Re-order player_indices to start with starting_player
    player_indices = player_indices[starting_player:] + player_indices[:starting_player]

    # Show initial board and first player
    clear_screen()
    print_board(board)
    print(f"Player {checkers[player_indices[0]]} begins!\n")

    # Gameplay loop
    turn = 0
    while True:
        curr_player = player_indices[turn % PLAYERS]
        curr_checker = checkers[curr_player]

        valid_cols = get_valid_columns(board)
        if not valid_cols:  # All columns full (should trigger draw elsewhere)
            print("No valid moves. The game is a draw!")
            break

        # Show board and prompt for move
        clear_screen()
        print_board(board)

        col_choice = get_player_input(valid_cols, curr_checker)

        # Place checker, if fails (column is full), lose the turn
        if not place_checker(board, col_choice, curr_checker):
            print(f"Column {string.ascii_uppercase[col_choice]} is full. Player {curr_checker} loses the turn!")
            input("Press Enter to continue...")
            turn += 1  # Advance to next player
            continue

        # After move, check if this player has won
        if check_win(board, curr_checker):
            clear_screen()
            print_board(board)
            print(f"Player {curr_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break

        # Next player's turn
        turn += 1

if __name__ == "__main__":
    main()
