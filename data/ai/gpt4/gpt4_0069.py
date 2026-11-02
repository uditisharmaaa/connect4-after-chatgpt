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
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col, board):
    return col.isalpha() and len(col) == 1 and "A" <= col <= chr(65 + COLS - 1) and board[0][ord(col) - 65] == " "

def drop_checker(board, col, checker):
    col_index = ord(col) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True

def check_winner(board, checker):
    # Horizontal
    for row in board:
        for c in range(COLS - 3):
            if row[c:c + 4] == [checker] * 4:
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if [board[r + i][c] for i in range(4)] == [checker] * 4:
                return True
    # Diagonal (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if [board[r + i][c + i] for i in range(4)] == [checker] * 4:
                return True
    # Diagonal (/)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if [board[r - i][c + i] for i in range(4)] == [checker] * 4:
                return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def connect_4():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        col = input().strip().upper()
        if not is_valid_column(col, board):
            print("Invalid input. Try again.")
            continue
        drop_checker(board, col, CHECKERS[current_player])
        if check_winner(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    connect_4()
