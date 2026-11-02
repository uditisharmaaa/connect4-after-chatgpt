import os
import random
import sys

# Constants for board dimensions
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # Max columns allowed, for flexibility if extended

# Constants for players and their checkers
PLAYERS_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players, only use first PLAYERS_COUNT

# Number of checkers in a row needed to win
WIN_LENGTH = 4

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create a board initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board with column headers and separators."""
    clear_screen()
    
    # Print column labels A, B, C, ...
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    
    # Print each row with separators
    for row in board:
        print('+' + '---+' * len(row))
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * len(board[0]))

def is_valid_column_input(column_input, columns):
    """Validate user input for column selection."""
    if len(column_input) != 1:
        return False
    letter = column_input.upper()
    if 'A' <= letter < chr(ord('A') + columns):
        return True
    return False

def column_index(column_letter):
    """Convert column letter to zero-based index."""
    return ord(column_letter.upper()) - ord('A')

def is_column_full(board, col_idx):
    """Check if the given column is full."""
    return board[0][col_idx] != ' '

def place_checker(board, checker, col_idx):
    """
    Place a checker in the specified column.
    Return True if placement successful, False if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    """Check all possible win directions for the given checker."""

    rows = len(board)
    cols = len(board[0])
    
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (down-right) check
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (up-right) check
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """Check if the board is completely full (draw)."""
    # If top row contains any space, game not draw
    return all(cell != ' ' for cell in board[0])

def main():
    # Validate constants limits
    if not (2 <= PLAYERS_COUNT <= 5):
        print(f"Error: PLAYERS_COUNT must be between 2 and 5")
        sys.exit(1)
    if not (1 <= ROWS and 1 <= COLUMNS <= MAX_COLUMNS):
        print(f"Error: Board size invalid")
        sys.exit(1)

    # Initialize board
    board = create_board(ROWS, COLUMNS)

    # Select random starting player
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    # Main game loop
    while True:
        print_board(board)
        current_checker = CHECKERS[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column_input(user_input, COLUMNS):
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
                continue
            col = column_index(user_input)
            # Check if column is full
            if is_column_full(board, col):
                # According to assignment: turn is lost if column is full
                print(f"Column {user_input} is full. You lose your turn.")
                break
            # Place checker
            placed = place_checker(board, current_checker, col)
            if placed:
                break
            else:
                # Should not normally happen because full check above
                print(f"Column {user_input} is full. You lose your turn.")
                break

        # Check win condition (only if placed successfully)
        if placed:
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                return

            # Check draw condition
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                return

        # Move to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
