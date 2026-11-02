import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2

CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(cols)))
    print("+---" * cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")

def is_valid_input(input_char, cols):
    if len(input_char) == 1 and 'A' <= input_char <= 'A' + chr(cols - 1):
        return True
    return False

def is_valid_move(board, col):
    return board[0][col] == " "

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            break

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal /
    for r in range(ROWS - 3):
        for c in range(3, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    checkers = CHECKERS[:PLAYERS]

    print_board(board, COLUMNS)

    while True:
        checker = checkers[current_player]
        while True:
            player_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            col = ord(player_input) - 65
            if is_valid_input(player_input, COLUMNS) and is_valid_move(board, col):
                break
            print("Invalid input. Please try again.")

        place_checker(board, col, checker)
        print_board(board, COLUMNS)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
