import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Get valid column from user
def get_valid_column(board, player):
    while True:
        column = input(f"Player {CHECKERS[player]}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha() or ord(column) - 65 not in range(COLUMNS):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_index = ord(column) - 65
        if board[0][col_index] != " ":
            print("Column is full. Choose a different column.")
            continue
        return col_index

# Place checker in column
def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = CHECKERS[player]
            break

# Check for win
def check_win(board, player):
    checker = CHECKERS[player]

    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == checker and all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game logic
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        # Get valid column from user and place checker
        column = get_valid_column(board, current_player)
        place_checker(board, column, current_player)

        # Print updated board
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
