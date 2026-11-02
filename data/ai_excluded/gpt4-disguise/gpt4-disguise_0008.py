import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Drop checker into the board
def drop_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

# Check win conditions
def check_winner(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Diagonal right
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Diagonal left
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if board[row][col] == checker and board[row + 1][col - 1] == checker and board[row + 2][col - 2] == checker and board[row + 3][col - 3] == checker:
                return True
    return False

# Check if the board is full
def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Get valid column from player input
def get_column_input():
    while True:
        col = input("Please enter a column: ").upper()
        if len(col) == 1 and "A" <= col <= chr(65 + COLUMNS - 1):
            return ord(col) - 65
        else:
            print("Invalid input. Try again.")

# Main game loop
def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, it's your turn!")
        col = get_column_input()
        
        if drop_checker(board, col, CHECKERS[current_player]):
            print_board(board)

            if check_winner(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if is_draw(board):
                print("It's a draw!")
                break

            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. Try another one.")

if __name__ == "__main__":
    main()
