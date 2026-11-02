import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    header = "  " + "   ".join(chr(65 + col) for col in range(COLUMNS))
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    """Checks if the given column is valid (A to G)."""
    return column.isalpha() and column.upper() >= "A" and column.upper() < chr(65 + COLUMNS)

def is_column_full(board, col_index):
    """Checks if the column is full."""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Places a checker in the specified column, if possible."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if a player has won."""
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

    # Diagonal (positive slope) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (negative slope) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is completely full."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Initialize the game
    board = create_board()
    turn = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_player = CHECKERS[turn]
        print(f"Player {current_player}, please enter a column:")
        player_input = input().strip()

        # Validate input
        if not is_valid_column(player_input):
            print("Invalid input. Please enter a valid column (e.g., A, B, C).")
            continue

        col_index = ord(player_input.upper()) - 65
        if is_column_full(board, col_index):
            print("Column is full. Please choose a different column.")
            continue

        # Place checker and update the board
        place_checker(board, col_index, current_player)
        print_board(board)

        # Check for a win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Alternate turn
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
