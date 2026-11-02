import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Initialize game board
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system("clear")
    print("  " + "   ".join(ALPHABET[:COLS]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column):
    return column in ALPHABET[:COLS] and board[0][ALPHABET.index(column)] == " "

def drop_checker(column, checker):
    col_idx = ALPHABET.index(column)
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            return

def check_winner(checker):
    # Check horizontal and vertical
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c:c + 4] == [checker] * 4: return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if [board[r + i][c] for i in range(4)] == [checker] * 4: return True
    # Check diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if [board[r + i][c + i] for i in range(4)] == [checker] * 4: return True
            if [board[r + 3 - i][c + i] for i in range(4)] == [checker] * 4: return True
    return False

def is_draw():
    return all(board[0][c] != " " for c in range(COLS))

def main():
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    print_board()
    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()
        if is_valid_column(column):
            drop_checker(column, current_player)
            print_board()
            if check_winner(current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw():
                print("The game is a draw!")
                break
            current_player = players[(players.index(current_player) + 1) % PLAYERS]
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
