import os
import random

# Constants (modifiable for board size and number of players)
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # maximum allowed columns
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Set game parameters (for submission: 6x7 board and 2 players)
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Allowed checkers in order

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create a 2D board initialized with white spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column letters and grid as shown in the assignment."""
    cols = len(board[0])
    rows = len(board)
    # Print column headers A, B, C, ..., depending on number of columns
    column_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(column_letters))
    # Print each row with borders
    for r in range(rows):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def is_valid_column_input(user_input, cols):
    """Check if user input is a valid column letter within the board."""
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    user_input = user_input.upper()
    first_col = 'A'
    last_col = chr(ord(first_col) + cols - 1)
    return first_col <= user_input <= last_col

def column_index_from_letter(letter):
    """Convert column letter to zero-based column index."""
    return ord(letter.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place the checker in the selected column: 
    start from bottom row and place checker in the lowest empty cell.
    Return True if successful, False if column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """
    Check for 4 consecutive checkers of the same type horizontally,
    vertically, and diagonally. Return True if such condition is met.
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

    # Diagonal "\" check (top-left to bottom-right)
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            # check 4 in this diagonal
            if all(board[r + i][c + i] == checker for i in range(needed)):
                return True

    # Diagonal "/" check (bottom-left to top-right)
    for r in range(needed - 1, rows):
        for c in range(cols - needed + 1):
            if all(board[r - i][c + i] == checker for i in range(needed)):
                return True

    return False

def board_full(board):
    """Check if all cells on the board are occupied (no ' ')."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Validate constants for safety
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return
    if COLUMNS > MAX_COLUMNS:
        print(f"Maximum supported columns is {MAX_COLUMNS}.")
        return
    if ROWS < 4 or COLUMNS < 4:
        print("Board must be at least 4x4 for the game to be playable.")
        return

    # Initialize board
    board = create_board(ROWS, COLUMNS)

    # Players and their checkers
    players_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board to user
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        checker = players_checkers[current_player]
        prompt = f"Player {checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(prompt).strip()
            if not is_valid_column_input(user_input, COLUMNS):
                # Invalid input, ask again
                continue
            col_idx = column_index_from_letter(user_input)
            # Check if column full
            if board[0][col_idx] != " ":
                # Column full -> player loses turn
                break
            else:
                # Place checker in column
                placed = place_checker(board, col_idx, checker)
                if not placed:
                    # This should not happen as we checked top cell,
                    # but just in case, treat as full column
                    break
                # Successful placement, exit input loop
                break

        clear_screen()
        print_board(board)

        # Check winner only if checker was placed (i.e. column not full)
        if board[0][col_idx] == checker:
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                return

        # Check for draw (board full)
        if board_full(board):
            print("The game is a draw!")
            return

        # Advance to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
