import os
import random

# Define constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def initialize_board(rows, cols):
    """Initializes the board with empty cells."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column labels (A, B, C, ...)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, cols):
    """Checks if a column input is valid."""
    return column.isalpha() and len(column) == 1 and 0 <= ord(column.upper()) - 65 < cols

def get_column_index(column):
    """Converts a column letter to its index."""
    return ord(column.upper()) - 65

def is_column_full(board, col_index):
    """Checks if a column is already full."""
    return all(row[col_index] != EMPTY_CELL for row in board)

def drop_checker(board, col_index, symbol):
    """Drops a player's checker in the specified column."""
    for row in reversed(board):
        if row[col_index] == EMPTY_CELL:
            row[col_index] = symbol
            return True
    return False  # This should never occur due to prior checks.

def check_winner(board, symbol):
    """Checks if the given symbol has won the game."""
    rows, cols = len(board), len(board[0])

    # Check horizontally
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == symbol:
                return True

    # Check vertically
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == symbol:
                return True

    # Check diagonals (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == symbol:
                return True

    # Check diagonals (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == symbol:
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(cell != EMPTY_CELL for row in board for cell in row)

def main():
    # Initialize the game settings
    board = initialize_board(ROWS, COLS)
    num_players = 2  # Requirement: Set to 2 players for submission
    players = PLAYER_SYMBOLS[:num_players]
    random.shuffle(players)
    turn = 0

    # Print initial board
    print_board(board)
    print(f"Randomly chosen to start: Player {players[turn]}")

    # Main game loop
    while True:
        print_board(board)
        current_player = players[turn]
        print(f"Player {current_player}, please enter a column:")

        # Validate input
        while True:
            column = input("Enter a column letter: ").strip()
            if not is_valid_column(column, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col_index = get_column_index(column)
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            break

        # Drop the checker
        drop_checker(board, col_index, current_player)

        # Check for a win or a draw
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch turns
        turn = (turn + 1) % num_players

if __name__ == "__main__":
    main()
