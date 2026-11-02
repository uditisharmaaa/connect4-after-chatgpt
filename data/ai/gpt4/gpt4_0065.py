import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Can be between 2 and 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board(rows, columns):
    """Initialize the game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the screen
    column_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS))
    separator = "+---" * COLUMNS + "+"
    print(column_labels)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(col, board):
    """Check if the column is valid for a move."""
    if len(col) != 1 or not col.isalpha():
        return False
    col_index = ord(col.upper()) - ord('A')
    return 0 <= col_index < COLUMNS and board[0][col_index] == " "

def drop_checker(col, board, symbol):
    """Drop the checker into the specified column."""
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return

def check_winner(board, symbol):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == symbol and \
               board[row][col + 1] == symbol and \
               board[row][col + 2] == symbol and \
               board[row][col + 3] == symbol:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == symbol and \
               board[row + 1][col] == symbol and \
               board[row + 2][col] == symbol and \
               board[row + 3][col] == symbol:
                return True

    # Check diagonals (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == symbol and \
               board[row + 1][col + 1] == symbol and \
               board[row + 2][col + 2] == symbol and \
               board[row + 3][col + 3] == symbol:
                return True

    # Check diagonals (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == symbol and \
               board[row - 1][col + 1] == symbol and \
               board[row - 2][col + 2] == symbol and \
               board[row - 3][col + 3] == symbol:
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Initialize game variables
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    print(f"Player {PLAYER_SYMBOLS[current_player]} goes first!")
    
    while True:
        # Print the board and prompt player
        print_board(board)
        column = input(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column: ").strip()

        # Validate input
        if not is_valid_column(column, board):
            print("Invalid input! Try again.")
            continue

        # Place checker
        drop_checker(column, board, PLAYER_SYMBOLS[current_player])

        # Check for win
        if check_winner(board, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
