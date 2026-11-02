import os
import random

# Constants for the game configuration
ROWS = 6               # Number of rows on the board
COLUMNS = 7            # Number of columns on the board (max 26)
NUM_PLAYERS = 2        # Number of players (between 2 and 5)
WIN_LENGTH = 4         # Number of checkers in a row needed to win
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players in order

# Validate the constants for safety
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
assert 1 <= ROWS and 1 <= COLUMNS <= 26, "Rows and columns must be positive, columns max 26"

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create a game board with empty spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels."""
    clear_screen()
    # Print column labels A, B, C, ...
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    # Print the board rows with borders
    row_separator = '+' + ('---+' * len(board[0]))
    for row in board:
        print(row_separator)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(row_separator)

def input_column(player_checker):
    """
    Prompt player for column input and validate.
    Returns the column index (0-based) if valid.
    """
    valid_columns = [chr(ord('A') + i) for i in range(COLUMNS)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Check input length and character
        if len(col_input) != 1 or col_input not in valid_columns:
            print(f"Invalid input! Please enter a letter from A to {valid_columns[-1]}.")
            continue
        col_index = ord(col_input) - ord('A')
        return col_index

def place_checker(board, col, checker):
    """
    Place a checker in the lowest available position in the given column.
    Returns True if placed successfully, False if the column is full.
    """
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    # Column full
    return False

def check_win(board, checker):
    """
    Check the board for any 4-in-a-row for the given checker.
    Returns True if found, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + offset][c] == checker for offset in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + offset][c + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-left)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r + offset][c - offset] == checker for offset in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Check if the board is full (no empty spaces).
    Returns True if full (draw), False otherwise.
    """
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize game board
    board = create_board(ROWS, COLUMNS)

    # Select players checkers for the current game
    players_checkers = CHECKERS[:NUM_PLAYERS]

    # Choose a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial empty board
    print_board(board)

    # Game loop
    while True:
        player_checker = players_checkers[current_player_index]

        # Prompt player for input and validate column choice
        col = input_column(player_checker)

        # Try to place checker
        placed = place_checker(board, col, player_checker)

        if not placed:
            # If the column is full, player loses a turn (no re-try)
            print(f"Column {chr(ord('A') + col)} is full. Player {player_checker} loses their turn.")
            # Wait a moment to let user see the message before continuing
            input("Press Enter to continue...")
        else:
            # Successfully placed checker: print updated board
            print_board(board)

            # Check for win
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break

            # Check for draw
            if check_draw(board):
                print("Game is a draw!")
                break

        # Rotate to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
