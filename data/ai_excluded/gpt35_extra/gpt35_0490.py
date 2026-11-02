import os
import random

# Constants for board dimensions and players
ROWS = 6       # number of rows
COLS = 7       # number of columns (max 26)
NUM_PLAYERS = 2  # between 2 and 5 inclusive
WIN_LENGTH = 4  # number of checkers in a row to win

# Player checkers in order, max 5 players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column labels A-G etc."""
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    print("  " + "   ".join(chr(ord('A') + i) for i in range(cols)))
    print("+" + "---+" * cols)
    for r in range(rows):
        print("| " + " | ".join(board[r][c] for c in range(cols)) + " |")
        print("+" + "---+" * cols)

def get_valid_column_input(current_player_checker, board):
    """Prompts player input until valid column is chosen."""
    cols = len(board[0])
    while True:
        print(f"Player {current_player_checker}, please enter a column:")
        user_input = input().strip().upper()
        # Validate length and character
        if len(user_input) != 1:
            # Invalid length
            continue
        col_char = user_input[0]
        if not ('A' <= col_char < chr(ord('A') + cols)):
            # Out of board column range
            continue
        col = ord(col_char) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full, player loses turn according to spec
            return None
        return col

def place_checker(board, col, checker):
    """
    Places the checker in the lowest available row in the given column.
    Returns True if placed successfully, False otherwise (shouldn't happen since we check full before)
    """
    rows = len(board)
    for r in range(rows-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the given checker has 4 in a row horizontally, vertically or diagonally."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full without any winner."""
    return all(cell != " " for cell in board[0])

def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Select players and their checkers
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly pick first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        col = get_valid_column_input(current_checker, board)
        if col is None:
            # Column full => turn lost
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place checker
        place_checker(board, col, current_checker)

        # Check win
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
