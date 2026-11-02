import os
import random
import string

# =========================
# Constants and Settings
# =========================
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2  # Must be between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]

assert 2 <= NUM_PLAYERS <= 5
assert COLUMNS <= MAX_COLUMNS

# =========================
# Board Functions
# =========================

def create_board():
    """Create an empty board (ROWS x COLUMNS) filled with spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board, current_player=None):
    """Clear the console and print the board."""
    os.system('clear')  # For Unix/Linux terminal

    # Print column labels
    labels = [string.ascii_uppercase[c] for c in range(COLUMNS)]
    print("  " + "   ".join(labels))
    print("+" + "---+" * COLUMNS)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)
    if current_player is not None:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

def get_column_index(user_input):
    """Given a user input letter, return the column index or None."""
    user_input = user_input.strip().upper()
    if len(user_input) == 1 and user_input in string.ascii_uppercase[:COLUMNS]:
        return ord(user_input) - ord('A')
    else:
        return None

def is_column_full(board, col):
    """Check if a column is completely filled."""
    return all(board[row][col] != " " for row in range(ROWS))

def place_checker(board, col, checker):
    """Place a checker in the given column. Return the row it was placed or None if column is full."""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Column is full

def get_valid_input(board, current_player):
    """Prompt player for a valid column input, repeat until valid."""
    while True:
        user_input = input()
        col = get_column_index(user_input)
        if col is None:
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        if is_column_full(board, col):
            print(f"Column {string.ascii_uppercase[col]} is full. You lose your turn.")
            return None  # Lose turn
        return col

# =========================
# Game Logic Functions
# =========================

def check_win(board, row, col, checker):
    """Check if placing checker at (row, col) resulted in a win"""
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Including the current checker
        # Check backward
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check forward
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Returns True if the board is full and nobody has won."""
    return all(board[0][col] != " " for col in range(COLUMNS))

# =========================
# Main Game Loop
# =========================

def main():
    board = create_board()
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]
    # Randomly pick starting player
    current_player = random.randint(0, num_players - 1)
    print_board(board, current_player)
    turn_count = 0

    while True:
        print_board(board, current_player)
        col = get_valid_input(board, current_player)
        if col is None:
            # Lose turn if column full
            current_player = (current_player + 1) % num_players
            continue
        row = place_checker(board, col, checkers[current_player])
        print_board(board, current_player)
        if check_win(board, row, col, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
