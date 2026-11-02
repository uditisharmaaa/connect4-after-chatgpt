import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
BOARD = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def check_input(input_str):
    if len(input_str) != 1:
        return False
    if not input_str.isalpha():
        return False
    column = ord(input_str.upper()) - ord('A')
    if column < 0 or column >= COLS:
        return False
    return True

def get_lowest_empty_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True
    # Check diagonal /
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True
    # Check diagonal \
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    players = 2
    current_player = random.randint(0, players - 1)

    while True:
        print_board(BOARD)
        print(f"Player {PLAYER_CHECKERS[current_player]}, please enter a column: ")
        user_input = input().strip().upper()

        if check_input(user_input):
            column = ord(user_input) - ord('A')
            if place_checker(BOARD, column, PLAYER_CHECKERS[current_player]):
                if check_win(BOARD, PLAYER_CHECKERS[current_player]):
                    print_board(BOARD)
                    print(f"Player {PLAYER_CHECKERS[current_player]} won!")
                    break
                if check_draw(BOARD):
                    print_board(BOARD)
                    print("It's a draw!")
                    break
                current_player = (current_player + 1) % players
            else:
                print("Column is full. Turn lost.")
        else:
            print("Invalid input. Please enter a valid column.")

main()
