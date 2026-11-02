import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2

# Checker symbols for players
CHECKERS = ["X", "O", "V", "H", "M"]

def init_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal down-left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == checker and board[row + 1][col - 1] == checker and board[row + 2][col - 2] == checker and board[row + 3][col - 3] == checker:
                return True

    return False

def check_draw(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    board = init_board()
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        move = input().strip().upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Try again.")
            continue
        col = ord(move) - 65
        if not is_valid_move(board, col):
            print("Column full or invalid. Try again.")
            continue
        
        drop_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
