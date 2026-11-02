import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
MAX_PLAYERS = 5

def clear_screen():
    os.system('clear')

def initialize_board(rows, cols):
    """Creates and returns a 2D board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board."""
    clear_screen()
    header = "  " + "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Checks if the column input is valid and has space."""
    if not column.isalpha() or len(column) != 1:  # Check single letter
        return False
    col_index = ord(column.upper()) - 65  # Convert letter to index
    if not (0 <= col_index < len(board[0])):  # Check range
        return False
    return board[0][col_index] == " "  # Check if there's space

def drop_checker(column, board, checker):
    """Drops the checker into the specified column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):  # Start from the bottom
        if row[col_index] == " ":
            row[col_index] = checker
            return

def check_winner(board, checker):
    """Checks if the given checker has 4 in a row."""
    rows, cols = len(board), len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right) check
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right) check
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is full (a draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game
    board = initialize_board(ROWS, COLUMNS)
    num_players = max(2, min(PLAYERS, MAX_PLAYERS))
    player_checkers = CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)  # Random start
    game_over = False

    print_board(board)

    while not game_over:
        current_checker = player_checkers[current_player]
        print(f"Player {current_checker}, please enter a column:")

        column = input().strip()
        while not is_valid_column(column, board):
            print("Invalid input. Please enter a valid column:")
            column = input().strip()

        drop_checker(column, board, current_checker)
        print_board(board)

        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % num_players  # Next player

if __name__ == "__main__":
    main()
