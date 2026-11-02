import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(c) for c in range(65, 65 + COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def check_input(user_input):
    if len(user_input) != 1 or not user_input.isalpha() or ord(user_input.upper()) - 65 >= COLS:
        return False
    return True

def place_checker(board, column, checker):
    col_idx = ord(column.upper()) - 65
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win_condition(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ")

        if not check_input(user_input):
            print("Invalid input, please try again.")
            continue

        if not place_checker(board, user_input, CHECKERS[current_player]):
            print("Column is full, try a different column.")
            continue

        print_board(board)

        if check_win_condition(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
