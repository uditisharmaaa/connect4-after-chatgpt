import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and column >= 'A' and column <= chr(65 + COLS - 1):
            col_index = ord(column) - 65
            if board[0][col_index] == " ":
                return col_index
            print("Column is full. Try again.")
        else:
            print("Invalid input. Please enter a letter from A to " + chr(65 + COLS - 1) + ".")

def drop_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_winner(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
if __name__ == "__main__":
    board = create_board()
    current_player = random.choice(PLAYERS)
    turns = 0

    while True:
        print_board(board)
        col_index = get_valid_column(current_player)
        drop_checker(board, col_index, current_player)
        turns += 1

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if turns >= ROWS * COLS:
            print_board(board)
            print("It's a draw!")
            break

        current_player = PLAYERS[turns % len(PLAYERS)]
