import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Global Variables
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
player_turn = 0


def clear_screen():
    os.system('clear')


def print_board():
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")


def get_valid_input():
    while True:
        try:
            column = input(f"Player {CHECKERS[player_turn]}, please enter a column: ")
            column_idx = ord(column.upper()) - 65
            if 0 <= column_idx < COLUMNS and board[0][column_idx] == " ":
                return column_idx
            print("Invalid input. Try again.")
        except (IndexError, ValueError):
            print("Invalid input. Try again.")


def place_checker(column_idx):
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][column_idx] == " ":
            board[row_idx][column_idx] = CHECKERS[player_turn]
            return True
    print(f"Column {chr(column_idx + 65)} is full. Turn lost.")
    return False


def check_winner():
    # Horizontal Check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != " ":
                return True
    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != " ":
                return True
    # Diagonal Check /
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != " ":
                return True
    # Diagonal Check \
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != " ":
                return True
    return False


def check_draw():
    return all(board[0][col] != " " for col in range(COLUMNS))


def connect4():
    global player_turn
    player_turn = random.randint(0, PLAYERS - 1)
    print_board()
    while True:
        column_idx = get_valid_input()
        if place_checker(column_idx):
            print_board()
            if check_winner():
                print(f"Player {CHECKERS[player_turn]} won!")
                break
            elif check_draw():
                print("The game is a draw!")
                break
            player_turn = (player_turn + 1) % PLAYERS


if __name__ == "__main__":
    connect4()
