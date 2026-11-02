import os
import random

# Constants to set board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Must be between 2 and 5

# Checkers for players in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board with column labels and borders."""
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    col_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(col_labels)

    # Print top border
    print("+" + "---+" * cols)

    for row in board:
        # Print each cell with vertical separators
        print("| " + " | ".join(row) + " |")
        # Print row border
        print("+" + "---+" * cols)

def is_valid_column(col_char, cols):
    """Check if column character is valid (within board columns)."""
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    return 'A' <= col_char <= chr(ord('A') + cols -1)

def column_index(col_char):
    """Convert column character (A-G) to index (0-6)."""
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in the chosen column at the lowest available row.
    Return True if placed, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """
    Check if the player with 'checker' has 4 in a row
    horizontally, vertically or diagonally.
    """
    rows = len(board)
    cols = len(board[0])
    needed = 4

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == needed:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == needed:
                    return True
            else:
                count = 0

    # Diagonal (down-right) check
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r+i][c+i] == checker for i in range(needed)):
                return True

    # Diagonal (up-right) check
    for r in range(needed - 1, rows):
        for c in range(cols - needed + 1):
            if all(board[r - i][c + i] == checker for i in range(needed)):
                return True

    return False

def check_draw(board):
    """Check if the board is full without any winner (draw)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Validate constants (optional sanity check)
    assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
    assert ROWS > 0 and COLS > 0 and COLS <= 26, "Invalid board dimensions"

    board = create_board(ROWS, COLS)

    # Assign players checkers according to NUM_PLAYERS
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly choose first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial empty board
    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        # Prompt player for input
        prompt = f"Player {current_checker}, please enter a column: "
        col_input = input(prompt).strip().upper()

        # Validate input - length 1, in range A to appropriate column
        while not (is_valid_column(col_input, COLS)):
            print(f"Invalid input! Please enter a column letter between A and {chr(ord('A') + COLS - 1)}.")
            col_input = input(prompt).strip().upper()

        col = column_index(col_input)

        # Try to place checker in the chosen column
        placed = place_checker(board, col, current_checker)

        if not placed:
            # Column full, player loses turn, print board and next player turn
            print_board(board)
            print(f"Column {col_input} is full. Player {current_checker} loses turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Successfully placed checker, print updated board
        print_board(board)

        # Check for win
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
