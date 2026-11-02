import os
import random

# -------- CONSTANTS --------
NUM_ROWS = 6         # Number of rows
NUM_COLS = 7         # Number of columns
PLAYERS = 2          # Number of players (2-5)
MAX_COLS = 26        # Maximum number of columns allowed
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols

# -------- FUNCTIONS --------

def clear_screen():
    os.system('clear')  # On Linux/Unix. Use 'cls' for Windows

def create_board(rows, cols):
    """Create a board with all whitespace."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Print the board with column letters."""
    # Column labels (A, B, ...)
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_column(cols, board):
    """Prompt user for a valid column letter input."""
    valid_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        choice = input().strip().upper()
        if choice in valid_letters:
            col_idx = ord(choice) - ord('A')
            # check if column is not full
            if board[0][col_idx] == ' ':
                return col_idx
            else:
                print("Column is full! You lose your turn.")
                return None  # Column full, lose turn
        else:
            print(f"Invalid input. Please enter a letter from {valid_letters[0]} to {valid_letters[-1]}:")

def drop_checker(board, col, checker):
    """Drop the checker in the selected column."""
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col  # return coordinates of the placed checker

def check_win(board, checker):
    # Horizontal check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal down-right
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal up-right
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Return True if the board is full, else False."""
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    # Use only allowed number of players and columns
    if PLAYERS < 2 or PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return
    if NUM_COLS < 1 or NUM_COLS > MAX_COLS:
        print(f"Number of columns must be between 1 and {MAX_COLS}.")
        return
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = PLAYER_CHECKERS[:PLAYERS]

    # Randomly choose first player
    current_player = random.randint(0, PLAYERS - 1)

    clear_screen()
    print_board(board, NUM_COLS)

    while True:
        checker = player_symbols[current_player]
        print(f"Player {checker}, please enter a column:")

        col = get_valid_column(NUM_COLS, board)
        if col is None:
            # Column is full, skip turn
            current_player = (current_player + 1) % PLAYERS
            continue

        row, col = drop_checker(board, col, checker)

        clear_screen()
        print_board(board, NUM_COLS)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        else:
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
