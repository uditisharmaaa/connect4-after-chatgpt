import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
current_player = random.choice(CHECKERS)


def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")


def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False


def is_valid_move(column):
    return 0 <= column < COLUMNS and board[0][column] == " "


def check_winner(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if c <= COLUMNS - 4:
                if all(board[r][c + i] == checker for i in range(4)):
                    return True
            if r <= ROWS - 4:
                if all(board[r + i][c] == checker for i in range(4)):
                    return True
            if r <= ROWS - 4 and c <= COLUMNS - 4:
                if all(board[r + i][c + i] == checker for i in range(4)):
                    return True
            if r <= ROWS - 4 and c >= 3:
                if all(board[r + i][c - i] == checker for i in range(4)):
                    return True
    return False


def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))


print_board(board)

while True:
    col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
    if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLUMNS - 1):
        column = ord(col_input) - 65
        if is_valid_move(column):
            drop_checker(board, column, current_player)
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
        else:
            print("Column is full, you lose your turn!")
    else:
        print("Invalid input, try again!")
