import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)) + "  ")
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(board, column):
    return0 <= column < COLUMNS and board[0][column] == " "

def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        column_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        if len(column_input) != 1 or not column_input.isalpha() or not is_valid_column(board, ord(column_input) - 65):
            print("Invalid input. Please try again.")
            continue

        column = ord(column_input) - 65    if place_checker(board, column, checker):
            print_board(board)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
