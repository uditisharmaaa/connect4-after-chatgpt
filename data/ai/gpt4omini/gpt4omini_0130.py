import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can add more characters for more players if needed

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)  # Top border of the board

    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row elements
        print("+" + "---+" * COLS)  # Row border

def is_valid_input(column):
    """Checks if the input column is valid."""
    return column in range(COLS)

def is_column_full(board, col):
    """Checks if a specified column is full."""
    return board[0][col] != " "  # If the topmost row of the column isn't empty

def drop_checker(board, col, checker):
    """Places the checker in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Checks for a win in the current board state."""
    # Check horizontal spaces
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    
    # Check vertical spaces
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (the board is full)."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    """Main function to manage the game flow."""
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select first player

    print("Starting the game! Player", current_player)
    print_board(board)

    while True:
        # Get valid column input
        while True:
            column_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()
            if len(column_input) != 1 or not column_input.isalpha():
                print("Invalid input! Please enter a letter from A to G.")
                continue
            col = ord(column_input) - 65  # Convert letter to column index
            if is_valid_input(col) and not is_column_full(board, col):
                break
            else:
                print("Column is either full or out of bounds. Try again.")

        # Place checker in the selected column
        drop_checker(board, col, current_player)
        print_board(board)

        # Check for a winning condition
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch players
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
