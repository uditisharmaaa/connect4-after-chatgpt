import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    column_labels = "   ".join(chr(65 + col) for col in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for valid input
def is_valid_input(column, columns_count):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < columns_count

# Get lowest empty row in a column
def get_lowest_empty_row(board, col_index):
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            return row_index
    return -1  # Column is full

# Check for win condition
def is_winner(board, checker):
    # Check horizontal, vertical, and diagonal patterns
    for row in range(ROWS):
        for col in range(COLUMNS - 3):  # Horizontal
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS):  # Vertical
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):  # Diagonal /
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):  # Diagonal \
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check if the board is full (draw condition)
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Select a random player to start
def random_start_player(players_count):
    return random.randint(0, players_count - 1)

# Main game logic
def play_game():
    board = create_board(ROWS, COLUMNS)
    players_count = PLAYERS
    current_player = random_start_player(players_count)
    checkers = CHECKERS[:players_count]

    print_board(board)

    while True:
        # Current player's turn
        print(f"Player {checkers[current_player]}'s turn!")
        column_input = input("Please enter a column: ").strip().upper()

        if not is_valid_input(column_input, COLUMNS):
            print("Invalid input. Please enter a valid column (e.g., A, B, C).")
            continue

        col_index = ord(column_input) - 65
        lowest_row = get_lowest_empty_row(board, col_index)

        if lowest_row == -1:
            print("Column is full. Try a different column.")
            continue

        # Place the checker
        board[lowest_row][col_index] = checkers[current_player]
        print_board(board)

        # Check for a win
        if is_winner(board, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch player
        current_player = (current_player + 1) % players_count

if __name__ == "__main__":
    play_game()
