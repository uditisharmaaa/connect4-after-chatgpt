import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    """Clears the screen."""
    os.system('clear')

def create_board():
    """Creates the game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col, board):
    """Checks if the column choice is valid."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def drop_checker(board, col, checker):
    """Drops the checker in the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return

def get_column_input(board):
    """Gets column input from player. Ensures valid input."""
    while True:
        try:
            col_input = input("Please enter a column (A-G): ").strip().upper()
            col = ord(col_input) - 65
            if col_input.isalpha() and is_valid_column(col, board):
                return col
            else:
                print("Invalid column! Please try again.")
        except (IndexError, ValueError):
            print("Invalid column! Please try again.")

def check_win(board, checker):
    """Checks if a player has won."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialization
    board = create_board()
    print_board(board)

    # Randomize first player
    current_player = random.randint(0, PLAYERS - 1)

    # Game loop
    while True:
        print(f"Player {CHECKERS[current_player]}'s turn.")
        col = get_column_input(board)
        drop_checker(board, col, CHECKERS[current_player])
        print_board(board)
        
        # Check for win
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
