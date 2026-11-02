import os
import random

# === GLOBAL CONSTANTS ===
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # Maximum columns (for labeling with A-Z)
PLAYERS = 2  # Set between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates and returns a board with given dimensions."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    columns = len(board[0])
    # Print column headers (A, B, ...)
    print('  ', end='')
    for col in range(columns):
        print(f' {chr(ord("A") + col)} ', end='')
    print()
    # Print top border
    print('+' + '---+' * columns)
    # Print rows
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        print('+' + '---+' * columns)

def is_valid_column(col_letter, columns):
    """Checks if the chosen column letter is valid."""
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha() or not col_letter.isupper():
        return False
    idx = ord(col_letter) - ord('A')
    return 0 <= idx < columns

def get_column_index(col_letter):
    """Converts a column letter to the board index."""
    return ord(col_letter) - ord('A')

def is_column_full(board, col_idx):
    """Checks if a column is full."""
    return board[0][col_idx] != ' '

def place_checker(board, col_idx, checker):
    """Places a checker in the specified column, if possible.
    Returns True if placed, False if column is full."""
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Checks for 4 in a row for the given checker."""
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal (down-right) check
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Diagonal (up-right) check
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    """Checks if the board is full (for a draw)."""
    return all(cell != ' ' for cell in board[0])

def get_valid_input(prompt, columns):
    """Prompts user for a valid column letter."""
    while True:
        col = input(prompt).strip().upper()
        if is_valid_column(col, columns):
            return col
        else:
            print("Invalid input! Please enter a valid column letter (e.g., A, B, ...).")

def main():
    # Initialize
    board = create_board(ROWS, COLUMNS)
    active_players = CHECKERS[:PLAYERS]
    cur_player = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        # Who is the current player
        checker = active_players[cur_player]
        print(f"Player {checker}, please enter a column:")
        col_letter = get_valid_input("> ", COLUMNS)
        col_idx = get_column_index(col_letter)

        # Check if column is full
        if is_column_full(board, col_idx):
            print("Column is full! Turn lost.")
            # Skip turn
            cur_player = (cur_player + 1) % PLAYERS
        else:
            # Place the checker
            place_checker(board, col_idx, checker)
            clear_screen()
            print_board(board)
            # Check for win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            # Check for draw
            if board_full(board):
                print("It's a draw!")
                break
            # Next player
            cur_player = (cur_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
