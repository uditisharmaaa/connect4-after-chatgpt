import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(i+65) for i in range(COLS)]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_column_choice():
    while True:
        choice = input("Please enter a column: ").strip().upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + COLS - 1):
            return ord(choice) - 65
        print("Invalid column. Try again.")

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_horizontal(board, checker):
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    return False

def check_vertical(board, checker):
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    return False

def check_diagonal(board, checker):
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def check_win(board, checker):
    return check_horizontal(board, checker) or check_vertical(board, checker) or check_diagonal(board, checker)

def main():
    board = create_board()
    players = list(range(PLAYERS))
    current_player = random.choice(players)

    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}'s turn.")
        col = get_column_choice()

        if place_checker(board, col, CHECKERS[current_player]):
            print_board(board)
            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column full. Try again.")

main()
