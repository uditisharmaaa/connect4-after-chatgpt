import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # A to G

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and returns an initialized game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_index(column_label):
    """Converts a column label (e.g., 'A') to the corresponding column index."""
    if column_label in COLUMN_LABELS:
        return COLUMN_LABELS.index(column_label)
    return -1

def is_valid_column(column, board):
    """Checks if the selected column is valid for a move."""
    col_index = get_column_index(column)
    return col_index != -1 and board[0][col_index] == " "

def place_checker(board, column, checker):
    """Places a checker in the lowest available row in the specified column."""
    col_index = get_column_index(column)
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Checks if the given player has won the game with 4 consecutive checkers."""
    # Check horizontally
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Check vertically
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonally (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonally (/ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is filled, leading to a draw."""
    return all(cell != " " for row in board for cell in row)

def get_valid_input(board):
    """Prompts the user for a valid column input."""
    while True:
        column = input("Please enter a column: ").strip().upper()
        if is_valid_column(column, board):
            return column
        print("Invalid input. Please try again.")

def main():
    # Initialize the game
    num_players = 2  # Default setup specifies 2 players
    players = PLAYER_CHECKERS[:num_players]
    board = create_board()
    current_player = random.choice(players)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {current_player}, it's your turn!")
        column = get_valid_input(board)
        place_checker(board, column, current_player)

        # Check for winner
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = players.index(current_player)
        current_player = players[(current_player_index + 1) % num_players]

if __name__ == "__main__":
    main()
