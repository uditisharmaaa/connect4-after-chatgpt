import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_NAMES = [chr(65 + i) for i in range(COLUMNS)]  # ['A', 'B', 'C', ...]

def create_board():
    """Create a 2D board initialized with whitespaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system("clear")
    print("  " + "   ".join(COLUMN_NAMES))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Check if the column is valid and not full."""
    if column not in COLUMN_NAMES:
        return False
    col_index = COLUMN_NAMES.index(column)
    return board[0][col_index] == " "  # Check if top row of column is empty

def drop_checker(column, checker, board):
    """Place the checker in the chosen column."""
    col_index = COLUMN_NAMES.index(column)
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_for_win(board, checker):
    """Check if the given checker has formed 4 in a row."""
    # Horizontal Check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical Check
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal (Top-Left to Bottom-Right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal (Bottom-Left to Top-Right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    # Initialize board and choose random first player
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts the game.")

    while True:
        # Current player's turn
        player_checker = CHECKERS[current_player]
        column = input(f"Player {player_checker}, please enter a column: ").upper()

        # Validate input
        if not is_valid_column(column, board):
            print("Invalid input. Please try again.")
            continue

        # Place checker
        drop_checker(column, player_checker, board)

        # Display updated board
        print_board(board)

        # Check for a win
        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for a draw
        if check_for_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
