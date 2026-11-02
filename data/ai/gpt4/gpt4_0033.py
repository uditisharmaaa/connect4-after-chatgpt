import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Only first `PLAYERS` used
MAX_COLS = 26  # Max columns allowed

def create_board(rows, cols):
    """Create the game board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the screen
    # Print column headers (A, B, C ...)
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, board):
    """Check if the column is valid for dropping a checker."""
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "  # Top of column must be empty

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    for row in range(len(board) - 1, -1, -1):  # Start from the bottom
        if board[row][column] == " ":
            board[row][column] = checker
            return

def check_winner(board, player):
    """Check if the player has won by forming 4 checkers in a row."""
    rows, cols = len(board), len(board[0])
    checker = CHECKERS[player]

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == checker:
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == checker:
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == checker:
                return True

    # Check diagonal (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if board[r][c] == board[r+1][c-1] == board[r+2][c-2] == board[r+3][c-3] == checker:
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces at the top row)."""
    return all(board[0][c] != " " for c in range(len(board[0])))

def main():
    # Initialize board and players
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}'s turn.")
        try:
            # Get column input from the player
            column_input = input("Enter a column (A-G): ").strip().upper()
            if len(column_input) != 1 or not column_input.isalpha():
                raise ValueError
            column = ord(column_input) - 65  # Convert letter to column index
        except ValueError:
            print("Invalid input. Please enter a valid column (e.g., A, B, C).")
            continue

        # Check if column is valid
        if not is_valid_column(column, board):
            print("Invalid column or column is full. Try again.")
            continue

        # Place the checker
        drop_checker(board, column, CHECKERS[current_player])

        # Check for a win
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
