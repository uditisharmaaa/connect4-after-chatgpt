import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]  # Handles maximum 5 players

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_input(input_char, cols):
    return len(input_char) == 1 and input_char.isalpha() and 65 <= ord(input_char) < 65 + cols

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][c] == checker for c in range(col, col + 4)):
                return True

    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[r][col] == checker for r in range(row, row + 4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect_four():
    board = initialize_board(ROWS, COLS)
    print_board(board)

    current_player = random.randint(0, PLAYERS - 1)
    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        column = input().strip().upper()

        if is_valid_input(column, COLS):
            column_index = ord(column) - 65
            if place_checker(board, column_index, current_checker):
                print_board(board)

                if check_win(board, current_checker):
                    print(f"Player {current_checker} won!")
                    break
                elif is_draw(board):
                    print("The game is a draw!")
                    break

                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column is full! Turn is lost.")
        else:
            print("Invalid input! Try again.")

if __name__ == "__main__":
    connect_four()
