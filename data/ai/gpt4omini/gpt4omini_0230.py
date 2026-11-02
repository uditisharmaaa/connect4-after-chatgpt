import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Extend this for more players if needed.

def create_board():
    """Create a 2D board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col):
    """Check if input is valid for column selection."""
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= chr(65 + COLS - 1)

def get_column_index(col):
    """Convert column character (A, B, ..., G) to index (0, 1, ..., 6)."""
    return ord(col.upper()) - 65

def drop_checker(board, col, checker):
    """Place the checker in the appropriate column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check for a win condition for the given checker."""
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal (\)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal (/)
                if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    """Check if the board is full indicating a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game function to run Connect 4."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip()

        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        col_index = get_column_index(user_input)

        if drop_checker(board, col_index, current_player):
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break

            if is_draw(board):
                print("The game is a draw!")
                break

            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]  # Switch player
        else:
            print("Column is full. Choose another column.")

if __name__ == "__main__":
    main()
