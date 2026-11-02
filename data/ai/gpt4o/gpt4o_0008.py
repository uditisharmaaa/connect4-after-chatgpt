import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    col_headers = "  ".join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {col_headers}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_choice():
    while True:
        choice = input("Please enter a column (e.g., A): ").strip().upper()
        if len(choice) == 1 and choice in [chr(i) for i in range(65, 65 + COLUMNS)]:
            return ord(choice) - 65
        print("Invalid input. Please enter a column letter corresponding to the available columns.")

def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False

def check_win(board, symbol):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == symbol for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == symbol for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == symbol for i in range(4)):
                return True

    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4():
    board = create_board()
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        print(f"Player {PLAYER_SYMBOLS[current_player]}'s turn")
        column = get_column_choice()
        if place_checker(board, column, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            if check_win(board, PLAYER_SYMBOLS[current_player]):
                print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. You lose your turn.")

if __name__ == "__main__":
    connect4()
