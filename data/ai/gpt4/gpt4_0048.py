import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Only "X" and "O" will be used for 2 players

def clear_screen():
    os.system('clear')

def create_board():
    """Creates a 2D list to represent the board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the Connect 4 board."""
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + col) for col in range(COLUMNS))
    print(column_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    """Checks if the column input is valid."""
    return column.isalpha() and len(column) == 1 and "A" <= column <= chr(65 + COLUMNS - 1)

def is_column_full(board, col_index):
    """Checks if a given column is full."""
    return board[0][col_index] != " "

def drop_checker(board, col_index, checker):
    """Drops the checker into the specified column at the lowest available space."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Checks if a player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
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
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Initialize game variables
    board = create_board()
    player_count = PLAYERS
    player_checkers = CHECKERS[:player_count]
    current_player = random.randint(0, player_count - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {player_checkers[current_player]}, it's your turn.")
        column_input = input("Please enter a column (A-G): ").strip().upper()

        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        col_index = ord(column_input) - 65

        if is_column_full(board, col_index):
            print("Column is full. Choose another column.")
            continue

        drop_checker(board, col_index, player_checkers[current_player])

        if check_winner(board, player_checkers[current_player]):
            print_board(board)
            print(f"Player {player_checkers[current_player]} won!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % player_count

if __name__ == "__main__":
    main()
