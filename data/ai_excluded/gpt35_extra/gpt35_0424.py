import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# For this assignment submission requirements:
NUM_PLAYERS = 2  # set number of players enabled here (range 2 to 5)
WIN_LENGTH = 4

PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constants
assert 1 < NUM_PLAYERS <= MAX_PLAYERS, "Number of players must be between 2 and 5."
assert 1 < COLUMNS <= MAX_COLUMNS, f"Columns must be between 2 and {MAX_COLUMNS}."
assert ROWS >= WIN_LENGTH, f"Rows must be at least {WIN_LENGTH} for a valid win."

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create and return a rows x cols board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    cols = len(board[0])
    header = "  "
    letters = string.ascii_uppercase
    for c in range(cols):
        header += f" {letters[c]}  "
    print(header)
    line = "+" + "---+" * cols
    for row in board:
        print(line)
        row_line = "|"
        for cell in row:
            row_line += f" {cell} |"
        print(row_line)
    print(line)

def input_column(player_char, cols):
    """Prompt the player for input until a valid column letter is entered."""
    letters = string.ascii_uppercase[:cols]
    while True:
        user_input = input(f"Player {player_char}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please input a single letter corresponding to a column.")
            continue
        if user_input not in letters:
            print(f"Invalid column. Please choose a letter between {letters[0]} and {letters[-1]}.")
            continue
        return letters.index(user_input)

def place_checker(board, col, player_char):
    """Place the checker in the lowest empty position in the specified column.
    If column is full, return False. Otherwise True."""
    # Start from bottom row going upwards
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = player_char
            return True
    return False

def check_win(board, player_char):
    rows = len(board)
    cols = len(board[0])
    length = WIN_LENGTH

    # Horizontal check
    for r in range(rows):
        for c in range(cols - length + 1):
            if all(board[r][c+i] == player_char for i in range(length)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - length + 1):
            if all(board[r+i][c] == player_char for i in range(length)):
                return True

    # Diagonal (down-right) check
    for r in range(rows - length + 1):
        for c in range(cols - length + 1):
            if all(board[r+i][c+i] == player_char for i in range(length)):
                return True

    # Diagonal (up-right) check
    for r in range(length - 1, rows):
        for c in range(cols - length + 1):
            if all(board[r - i][c + i] == player_char for i in range(length)):
                return True

    return False

def board_full(board):
    """Check if board is full (no empty spaces)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)

    players = PLAYERS_CHECKERS[:NUM_PLAYERS]

    # Choose random player index to start
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_char = players[current_player_idx]

        col = input_column(player_char, COLUMNS)

        placed = place_checker(board, col, player_char)
        if not placed:
            # If column full, player loses turn
            print(f"Column {string.ascii_uppercase[col]} is full. Player {player_char} loses their turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, player_char):
            print(f"Player {player_char} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
