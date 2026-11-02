import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear') if os.name != 'nt' else os.system('cls')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < COLUMNS

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_winner(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    for r in range(ROWS-3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        column = input(f"Player {checker}, please enter a column: ").upper()

        if not is_valid_input(column):
            print("Invalid input. Try again.")
            continue

        col_index = ord(column) - 65

        if not place_checker(board, col_index, checker):
            print("Column full. Turn lost.")
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        if is_draw(board):
            print("Game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
