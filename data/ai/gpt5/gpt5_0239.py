import os
import random
import string
import sys

# -----------------------------
# Configuration (submission requires 6x7 and 2 players)
# -----------------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player checker symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# -----------------------------
# Validation of configuration
# -----------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)

# -----------------------------
# Board utilities
# -----------------------------
def create_board(rows, cols):
    """Create a rows x cols board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clear terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the board with column labels as shown in the assignment."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal separator line for one row
    separator = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(separator)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(separator)

def letter_to_col(letter):
    """Convert a column letter (A..Z) to a 0-based column index."""
    letter = letter.upper()
    if len(letter) != 1 or letter < 'A' or letter > 'Z':
        return None
    return ord(letter) - ord('A')

def is_valid_column_letter(letter, max_cols):
    """Check if input letter is valid and within the board column range."""
    if len(letter) != 1:
        return False
    ch = letter.upper()
    if not ('A' <= ch <= 'Z'):
        return False
    col = ord(ch) - ord('A')
    return 0 <= col < max_cols

def column_full(board, col):
    """Return True if the column is completely filled."""
    return board[0][col] != " "

def place_checker(board, col, symbol):
    """
    Place a checker with 'symbol' into column 'col'.
    Returns (success, (row, col)) where success is True if placed.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True, (r, col)
    return False, None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, last_row, last_col, symbol):
    """
    Check if placing 'symbol' at (last_row, last_col) created a 4-in-a-row.
    Checks horizontal, vertical, and two diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count includes the last placed checker

        # Extend in positive direction
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Extend in negative direction
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def board_full(board):
    """Return True if no spaces remain on the board (draw)."""
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

# -----------------------------
# Game loop
# -----------------------------
def main():
    board = create_board(ROWS, COLS)

    # Determine player symbols based on NUM_PLAYERS
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    winner = None

    while True:
        current_symbol = players[current_player_index]

        # Prompt until we get a syntactically valid input (letter within range)
        while True:
            prompt = f"Player {current_symbol}, please enter a column: "
            user_input = input(prompt).strip()
            if is_valid_column_letter(user_input, COLS):
                break
            else:
                # Invalid input (e.g., numbers, invalid char, out of board)
                print("Invalid input. Please enter a valid column letter.")

        col = letter_to_col(user_input)

        # If the chosen column is full, the turn is invalid and player loses the turn
        if column_full(board, col):
            # Show message and move to next player without placing a checker
            print("Column is full. You lose your turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

            # Show updated board (no change but still reprint per spec)
            input("Press Enter to continue...")
            clear_screen()
            print_board(board)
            continue

        # Place checker
        placed, (r, c) = place_checker(board, col, current_symbol)
        # placed should be True because we checked column_full above
        # Print updated board
        clear_screen()
        print_board(board)

        # Check for win condition after a successful placement
        if placed and check_win(board, r, c, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End of game

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame terminated.")
        sys.exit(0)
