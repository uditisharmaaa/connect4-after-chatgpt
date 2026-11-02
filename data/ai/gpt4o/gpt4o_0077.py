import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

# Initialize board
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')  # Clear the terminal
    column_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS))
    print(column_labels)
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def drop_checker(column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                if all(board[row][col + i] == checker for i in range(4) if col + i < COLUMNS):  # Horizontal
                    return True
                if all(board[row + i][col] == checker for i in range(4) if row + i < ROWS):  # Vertical
                    return True
                if all(board[row + i][col + i] == checker for i in range(4) if row + i < ROWS and col + i < COLUMNS):  # Diagonal /
                    return True
                if all(board[row + i][col - i] == checker for i in range(4) if row + i < ROWS and col - i >= 0):  # Diagonal \
                    return True
    return False

def check_draw():
    return all(cell != " " for row in board for cell in row)

def get_column():
    while True:
        inp = input("Player {}, please enter a column: ".format(CHECKERS[current_player]))
        if len(inp) == 1 and inp.isalpha():
            column = ord(inp.upper()) - ord('A')
            if 0 <= column < COLUMNS:
                return column
        print("Invalid input. Try again.")

current_player = random.randint(0, PLAYERS - 1)
print_board()

while True:
    column = get_column()
    if drop_checker(column, CHECKERS[current_player]):
        print_board()
        if check_win(CHECKERS[current_player]):
            print("Player {} won!".format(CHECKERS[current_player]))
            break
        if check_draw():
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS
    else:
        print("Column full. Player loses turn.")
