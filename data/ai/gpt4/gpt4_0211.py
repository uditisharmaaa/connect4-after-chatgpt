import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]

def create_board():
    """Create an empty board initialized with spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(column, board):
    """Check if a player’s input is valid."""
    if column.isalpha() and len(column) == 1:
        col_idx = ord(column.upper()) - 65
        if 0 <= col_idx < COLUMNS and board[0][col_idx] == " ":
            return True
    return False

def drop_checker(board, column, checker):
    """Place the checker in the lowest available row in the given column."""
    col_idx = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            break

def check_winner(board, checker):
    """Check if the current player has won the game."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (if the board is full)."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Initialize board and select the first player randomly
    board = create_board()
    current_player = random.randint(0, PLAYER_COUNT - 1)

    # Main game loop
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, it's your turn!")

        # Get player input
        column = input("Please enter a column: ").strip()
        if not is_valid_input(column, board):
            print("Invalid input. Please try again.")
            continue

        # Drop the checker
        drop_checker(board, column, CHECKERS[current_player])

        # Check for win or draw
        if check_winner(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won! Congratulations!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
