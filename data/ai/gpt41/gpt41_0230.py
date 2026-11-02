import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Change to 3, 4, or 5 for more players (max 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Creates a 2D board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(LETTERS))
    # Print top border
    print("+" + "---+" * COLS)
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_columns(board):
    """Returns a list of indices of columns that are not full."""
    valid = []
    for c in range(COLS):
        if board[0][c] == ' ':
            valid.append(c)
    return valid

def is_column_full(board, col):
    """Returns True if column is full."""
    return board[0][col] != ' '

def get_input(board, player_num):
    """Ask for user input and validate."""
    valid_cols = get_valid_columns(board)
    valid_letters = [LETTERS[c] for c in valid_cols]
    checker = CHECKERS[player_num]
    while True:
        inp = input(f"Player {checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in LETTERS:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = LETTERS.index(inp)
        if is_column_full(board, col):
            print("Sorry, that column is full. You lose your turn!")
            return None   # Lose turn if column is full
        return col

def place_checker(board, col, checker):
    """Place checker in column col."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not happen if validated

def check_win(board, checker):
    """Check for four in a row horizontally, vertically, or diagonally."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Check diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if board is full."""
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    print(f"Player {CHECKERS[current_player]} goes first!")
    input("Press Enter to start...")

    while True:
        print_board(board)
        col = get_input(board, current_player)
        if col is None:
            # Column full, lose turn
            current_player = (current_player + 1) % PLAYERS
            continue
        checker = CHECKERS[current_player]
        row, _ = place_checker(board, col, checker)
        # Check for win
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
