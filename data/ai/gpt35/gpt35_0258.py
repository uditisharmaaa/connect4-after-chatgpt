import os
import random

# Constants for board size and players
ROWS = 6             # Number of rows
COLS = 7             # Number of columns
NUM_PLAYERS = 2      # Number of players (between 2 and 5)
WIN_LENGTH = 4       # Number of checkers needed in a row to win
CHECKERS = ["X", "O", "V", "H", "M"]  # Available checkers for players

def clear_screen():
    """Clear terminal screen using 'clear' command."""
    os.system('clear')

def create_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board with column labels."""
    clear_screen()
    # Print column labels: A, B, C, ...
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print the board with borders
    for row in range(len(board)):
        print("+" + "---+" * len(board[0]))
        row_str = "|"
        for col in range(len(board[0])):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print("+" + "---+" * len(board[0]))

def is_valid_column(col_char, cols):
    """Check if the input column character is valid for the board."""
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if 'A' <= col_char <= chr(ord('A') + cols - 1):
        return True
    return False

def get_column_index(col_char):
    """Convert column letter to zero-based index."""
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Attempt to place the checker into the specified column.
    The checker falls to the lowest empty row.
    If column full, return False.
    Otherwise, place checker and return True.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """
    Check if the given checker has a winning position:
    4 in a row horizontally, vertically, or diagonally.
    Returns True if winner found, else False.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-left)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r+i][c-i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def is_board_full(board):
    """Check if the board is completely filled (no empty spaces)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Setup game variables
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly pick first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        checker = players_checkers[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        input_valid = False
        col_idx = None

        # Get valid input from player
        while not input_valid:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, COLS):
                # Invalid input: not a valid column label
                continue
            col_idx = get_column_index(user_input)
            # Check if column full before placing
            if board[0][col_idx] != " ":
                # Column full - lose turn, invalid move
                # Show board and move to next player
                print_board(board)
                print(f"Column {user_input} is full. Player {checker} loses the turn.")
                col_idx = None  # No placement done this turn
                break
            else:
                # Valid placement
                input_valid = True

        # Place checker if valid column and not full
        if col_idx is not None:
            place_checker(board, col_idx, checker)

        # Print board after move or lost turn
        print_board(board)

        # Check win only if checker placed
        if col_idx is not None and check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if is_board_full(board):
            print("Game ended in a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
