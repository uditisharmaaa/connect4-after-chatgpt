import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# Create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if a column is valid and not full
def is_valid_column(board, column):
    return column in COLUMN_LABELS and board[0][COLUMN_LABELS.index(column)] == " "

# Place a checker in the specified column
def place_checker(board, column, checker):
    col_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

# Check for a win
def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check if the board is full
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def play_game():
    # Initialize the board
    board = create_board()

    # Select active players' checkers
    active_checkers = CHECKERS[:PLAYERS]

    # Randomly choose the first player
    current_player = random.randint(0, PLAYERS - 1)

    # Game loop
    while True:
        # Print the board
        print_board(board)

        # Current player's turn
        print(f"Player {active_checkers[current_player]}, please enter a column:")
        column = input().strip().upper()

        # Validate input
        if not is_valid_column(board, column):
            print("Invalid input. Try again.")
            continue

        # Place the checker
        place_checker(board, column, active_checkers[current_player])

        # Check for a win
        if check_winner(board, active_checkers[current_player]):
            print_board(board)
            print(f"Player {active_checkers[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
