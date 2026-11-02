import os
import random

# Constant variables for the Connect 4 game
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Allowing up to 5 players

def create_board():
    """Create a 2D board initialized with whitespaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen for better visuals
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers A-G
    print("+" + "---+" * COLS)  # Print top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Print boundary after each row

def choose_first_player():
    """Randomly choose the first player."""
    return random.randint(0, len(PLAYERS) - 1)

def is_valid_input(col):
    """Check if the column input is valid."""
    return col.isalpha() and 'A' <= col.upper() <= chr(65 + COLS - 1)

def get_column_index(col):
    """Convert column letter to index."""
    return ord(col.upper()) - 65

def drop_checker(board, column, checker):
    """Drop a checker into the chosen column if valid."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check for a win in the board for a given checker."""
    # Check horizontal, vertical, and diagonal (both)
    
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):  # Avoid out of bounds
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):  # Avoid out of bounds
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Diagonal check (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Diagonal check (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = choose_first_player()

    print_board(board)

    while True:
        checker = PLAYERS[current_player]
        column = input(f"Player {checker}, please enter a column (A-G): ").strip()

        if not is_valid_input(column):
            print("Invalid input, please try again.")
            continue

        column_index = get_column_index(column)
        if not drop_checker(board, column_index, checker):
            print("Column is full, please choose another column.")
            continue

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    main()
