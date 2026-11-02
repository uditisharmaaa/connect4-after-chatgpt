import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # You can modify this for more players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    header = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    print(header)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_column_choice():
    while True:
        choice = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        if len(choice) == 1 and 'A' <= choice <= 'G':
            column = ord(choice) - ord('A')
            return column
        print("Invalid input. Please enter a letter from A to G.")

def place_checker(board, column):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = current_player
            return True
    return False

def check_winner(board):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != " ":
                if (check_horizontal(board, r, c) or
                    check_vertical(board, r, c) or
                    check_diagonal(board, r, c)):
                    return True
    return False

def check_horizontal(board, r, c):
    count = 0
    for i in range(COLS):
        if board[r][i] == board[r][c]:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_vertical(board, r, c):
    count = 0
    for i in range(ROWS):
        if board[i][c] == board[r][c]:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_diagonal(board, r, c):
    return (check_diagonal_lr(board, r, c) or
            check_diagonal_rl(board, r, c))

def check_diagonal_lr(board, r, c):
    count = 0
    for i in range(-3, 4):
        if 0 <= r + i < ROWS and 0 <= c + i < COLS:
            if board[r + i][c + i] == board[r][c]:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

def check_diagonal_rl(board, r, c):
    count = 0
    for i in range(-3, 4):
        if 0 <= r + i < ROWS and 0 <= c - i < COLS:
            if board[r + i][c - i] == board[r][c]:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main Game Loop
if __name__ == "__main__":
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        column = get_column_choice()
        if place_checker(board, column):
            print_board(board)
            if check_winner(board):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full, please choose another column.")
