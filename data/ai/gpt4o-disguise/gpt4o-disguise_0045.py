import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O']

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))]))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(input, cols):
    return len(input) == 1 and input.isalpha() and ord(input.upper()) >= ord('A') and ord(input.upper()) < ord('A') + cols

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def is_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if col + 3 < COLS and all(board[row][col+i] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and all(board[row+i][col] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and col + 3 < COLS and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and col - 3 >= 0 and all(board[row+i][col-i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()

        if not is_valid_input(user_input, COLS):
            print("Invalid input, try again.")
            continue

        col = ord(user_input) - ord('A')
        if not place_checker(board, col, CHECKERS[current_player]):
            print("Column is full, turn lost.")
        else:
            print_board(board)

            if is_winner(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if is_draw(board):
                print("Game is a draw!")
                break

        current_player = (current_player + 1) % PLAYERS

main()
