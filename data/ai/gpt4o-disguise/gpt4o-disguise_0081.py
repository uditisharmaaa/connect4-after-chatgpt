import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = [chr(65 + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_input():
    while True:
        player_input = input("Player {}, please enter a column: ".format(CHECKERS[current_player]))
        if len(player_input) == 1 and 'A' <= player_input <= chr(64 + COLS):
            return ord(player_input) - 65
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_for_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

board = create_board(ROWS, COLS)
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

while True:
    col = get_valid_input()
    if place_checker(board, col, CHECKERS[current_player]):
        print_board(board)
        if check_for_winner(board, CHECKERS[current_player]):
            print("Player {} won!".format(CHECKERS[current_player]))
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS
    else:
        print("Column full, turn lost!")
