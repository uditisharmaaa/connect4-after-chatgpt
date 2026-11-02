import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
SYMBOLS = ['X', 'O']

def init_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_column_index():
    while True:
        col = input(f"Player {SYMBOLS[current_player]}, please enter a column: ").upper()
        if col in column_labels and not board[0][column_labels.index(col)] != ' ':
            return column_labels.index(col)
        print("Invalid input. Try again.")

def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return

def check_winner(board):
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == current_symbol and all(board[row][col + i] == current_symbol for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == current_symbol and all(board[row + i][col] == current_symbol for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == current_symbol and all(board[row + i][col + i] == current_symbol for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == current_symbol and all(board[row - i][col + i] == current_symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])

board = init_board()
column_labels = [chr(65 + i) for i in range(COLUMNS)]
current_player = random.randint(0, PLAYERS - 1)

while True:
    print_board(board)
    current_symbol = SYMBOLS[current_player]
    column_choice = get_column_index()
    place_checker(board, column_choice, current_symbol)
    if check_winner(board):
        print_board(board)
        print(f"Player {current_symbol} won!")
        break
    if check_draw(board):
        print_board(board)
        print("The game is a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
