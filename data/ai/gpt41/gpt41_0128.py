import os
import random
import string

# ------------------ CONSTANTS ------------------
NUM_ROWS = 6              # Default: 6
NUM_COLS = 7              # Default: 7
MAX_COLS = 26             # Max 26 columns, for A-Z
PLAYERS = 2               # Number of players (2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']


# ------------------ BOARD FUNCTIONS ------------------

def create_board(rows, cols):
    """Create an empty board with given rows and cols."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board."""
    os.system('clear')  # For Linux/Unix; use 'cls' for Windows

    cols = len(board[0])
    # Print Column Headers (A, B, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)

    # Print the horizontal separator line
    separator = "+" + "---+" * cols
    print(separator)

    for row in board:
        row_display = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_display)
        print(separator)

# ------------------ INPUT VALIDATION ------------------

def get_valid_column(board, current_checker):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in valid_letters:
            print(f"Invalid input! Please enter a letter from {valid_letters[0]} to {valid_letters[-1]}.")
            continue
        col = ord(user_input) - ord('A')
        # Check if the column is full
        if board[0][col] != " ":
            print("This column is full! You lose your turn.")
            return None  # Signal the column is full and turn is lost
        return col

# ------------------ GAME LOGIC ------------------

def drop_checker(board, col, checker):
    """Drop the checker into the given column and return the row where it landed."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should not reach here if validated outside
    return None

def is_winner(board, checker):
    """Check for a win for 'checker'."""
    rows, cols = len(board), len(board[0])

    # Directions: [(dx, dy)]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Down, Right, Down-right, Down-left

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    nr += dr
                    nc += dc
    return False

def is_full(board):
    """Return True if board is full, else False."""
    return all(cell != " " for cell in board[0])

# ------------------ MAIN GAME FUNCTION ------------------

def main():
    # Initialize the board
    rows, cols = NUM_ROWS, NUM_COLS
    board = create_board(rows, cols)

    # Setup player checkers
    num_players = PLAYERS
    checkers = CHECKERS[:num_players]

    # Randomize player order
    current_player_index = random.randint(0, num_players - 1)
    current_checker = checkers[current_player_index]

    print_board(board)

    game_ended = False
    while not game_ended:
        col = get_valid_column(board, current_checker)
        if col is None:
            # Column is full -- lose turn, so switch players
            current_player_index = (current_player_index + 1) % num_players
            current_checker = checkers[current_player_index]
            print_board(board)
            continue

        # Drop the checker
        drop_checker(board, col, current_checker)

        # Print updated board
        print_board(board)

        # Check win
        if is_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if is_full(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players
        current_checker = checkers[current_player_index]

if __name__ == "__main__":
    main()
