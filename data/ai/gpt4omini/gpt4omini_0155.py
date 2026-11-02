import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a new game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_next_empty_row(board, col):
    """Return the next available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1  # Column is full

def is_valid_input(column):
    """Check if the input column is valid (e.g., A-G)."""
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(64 + COLS)

def place_checker(board, row, col, checker):
    """Place a checker on the board in the specified location."""
    board[row][col] = checker

def check_winner(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Setup game
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_checker = PLAYERS[current_player_index]
        col_input = input(f"Player {current_checker}, please enter a column (A-{chr(64 + COLS)}): ").upper()

        # Validate input
        while not is_valid_input(col_input):
            col_input = input(f"Invalid input. Player {current_checker}, please enter a column (A-{chr(64 + COLS)}): ").upper()

        col = ord(col_input) - 65  # Convert column letter to index
        row = get_next_empty_row(board, col)  # Find next empty row

        if row == -1:  # Column is full
            print("Column is full! Try again.")
            continue

        place_checker(board, row, col, current_checker)  # Place the checker
        print_board(board)

        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch players

if __name__ == "__main__":
    main()
