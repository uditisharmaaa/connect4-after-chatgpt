import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # Adjust for more players (max 5)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]  # Checker symbols for players
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', ..., 'G']

def initialize_board(rows, cols):
    """Creates an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(COLUMN_LABELS))  # Column headers
    print("+" + "---+" * COLUMNS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)  # Separator border

def is_valid_column(col, board):
    """Checks if the selected column is valid and not full."""
    return col in COLUMN_LABELS and any(row[COLUMN_LABELS.index(col)] == " " for row in board)

def drop_checker(board, col, checker):
    """Drops the player's checker into the selected column."""
    col_index = COLUMN_LABELS.index(col)
    for row in reversed(board):  # Start from the bottom row
        if row[col_index] == " ":
            row[col_index] = checker
            return

def check_win(board, checker):
    """Checks if the given checker has 4 in a row (horizontally, vertically, or diagonally)."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to play the Connect 4 game."""
    board = initialize_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)  # Randomly select the first player

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        col = input().strip().upper()  # Get user input

        if not is_valid_column(col, board):
            print("Invalid input. Please enter a valid column.")
            continue

        drop_checker(board, col, current_player)

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = players.index(current_player)
        current_player = players[(current_player_index + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
