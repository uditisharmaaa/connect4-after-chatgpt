import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players

# Initialize the board
def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+---" * COLUMNS + "+")

# Check for a win condition
def check_winner(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True

    # Diagonal (\) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True

    # Diagonal (/) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Place a checker in a column
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

# Validate input
def valid_input(char):
    if len(char) != 1:
        return False
    if ord(char) < 65 or ord(char) >= 65 + COLUMNS:
        return False
    return True

# Main game loop
def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = CHECKERS[current_player]

        print(f"Player {current_checker}, please enter a column (A-{chr(64 + COLUMNS)}):")
        col_input = input().strip().upper()

        if not valid_input(col_input):
            print("Invalid input, try again.")
            continue

        col = ord(col_input) - 65

        if not place_checker(board, col, current_checker):
            print("Column full, try again.")
            continue

        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
