import os
import random

# Constants
ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_column(column, board):
    return 0 <= column < COLS and board[0][column] == " "

def find_next_open_row(column, board):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            return row
    return None

def place_checker(column, checker, board):
    row = find_next_open_row(column, board)
    if row is not None:
        board[row][column] = checker
        return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = PLAYER_CHECKERS[current_player]
        while True:
            col_str = input(f"Player {checker}, please enter a column: ")
            if col_str.isalpha() and len(col_str) == 1:
                column = ord(col_str.upper()) - 65
                if is_valid_column(column, board):
                    break
            print("Invalid input. Please try again.")
        
        if place_checker(column, checker, board):
            print_board(board)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
