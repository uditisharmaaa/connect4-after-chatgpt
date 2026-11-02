import os
import random

# Constants - Board dimensions and players
ROWS = 6           # Number of rows in the board
COLS = 7           # Number of columns in the board (max 26)
PLAYERS = 2        # Number of players (2 to 5)
WIN_CONDITION = 4  # Number of consecutive checkers needed to win

# Checkers assigned to players in order
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create and return a 2D board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the board to the screen with column labels.
    The top row lists columns A-G, rows below display the board cells.
    """
    cols = len(board[0])
    # Print column labels (A, B, C, ...)
    col_labels = '  ' + '   '.join(chr(ord('A') + i) for i in range(cols))
    print(col_labels)
    # Print horizontal separator line
    sep_line = '+' + '---+' * cols
    for row in board:
        print(sep_line)
        # Print row content with vertical bars between cells
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(sep_line)  # Bottom line

def get_valid_column_input(board, player_checker):
    """
    Prompt the current player to enter a column letter.
    Validate input: single uppercase letter in range and convert to column index.
    If input is invalid, keep asking without losing turn.
    """
    cols = len(board[0])
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Validate length and character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter (A-G).")
            continue
        col = ord(user_input) - ord('A')
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        return col

def place_checker(board, col, checker):
    """
    Place the player's checker in the chosen column.
    The checker falls to the lowest empty spot in the column.
    If column is full, return False indicating invalid move (loses turn).
    Otherwise, place checker and return True.
    """
    rows = len(board)
    # Start checking from bottom row upwards
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    # Column full
    return False

def check_winner(board, checker):
    """
    Check if the player with 'checker' has a winning condition.
    Win conditions checked:
    - Horizontal (left to right)
    - Vertical (top to bottom)
    - Diagonal (2 directions)
    Return True if win found, otherwise False.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r+i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def is_board_full(board):
    """Return True if the board is full (no empty spaces), else False."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Select players checkers based on number of players
    player_checkers = PLAYER_CHECKERS[:PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = player_checkers[current_player_idx]

        # Get and validate player input column, no turn lost for invalid input here
        col = get_valid_column_input(board, current_checker)

        # Try placing the checker in the column
        placed = place_checker(board, col, current_checker)
        if not placed:
            # Column full, turn lost for this player as per assignment instructions
            # Print message, then switch player
            print(f"Column {chr(ord('A') + col)} is full! Player {current_checker} loses this turn.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        # After placement, check for a winner
        if check_winner(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw (board full)
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
