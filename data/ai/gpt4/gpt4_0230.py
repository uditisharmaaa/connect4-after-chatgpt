import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(65 + i) for i in range(COLUMNS)]  # ['A', 'B', 'C', ...]

def create_board(rows, columns):
    """Creates an empty board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(COLUMN_LABELS[:COLUMNS]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if the column input is valid."""
    return column in COLUMN_LABELS[:COLUMNS] and any(row[COLUMN_LABELS.index(column)] == " " for row in board)

def place_checker(board, column, checker):
    """Places a checker in the specified column."""
    col_index = COLUMN_LABELS.index(column)
    for row in reversed(board):  # Start from the bottom
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Checks if a player has won the game."""
    # Check horizontal wins
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical wins
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

def is_draw(board):
    """Checks if the board is full."""
    return all(cell != " " for row in board for cell in row)

def get_player_input(player, board):
    """Prompts the player for input and validates it."""
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if is_valid_column(column, board):
            return column
        print("Invalid column. Try again.")

def main():
    """Main function that runs the Connect 4 game."""
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS_COUNT]
    current_player = random.choice(players)  # Randomly select the starting player

    print_board(board)
    print(f"Player {current_player} starts!\n")

    while True:
        # Get valid input from the current player
        column = get_player_input(current_player, board)

        # Place the checker and print the updated board
        place_checker(board, column, current_player)
        print_board(board)

        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS_COUNT]

if __name__ == "__main__":
    main()
