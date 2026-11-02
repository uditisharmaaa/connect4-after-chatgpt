import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board():
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def is_valid_move(col):
    return board[0][col] == ' '

def make_move(player, col):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def check_win(player):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == player:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == player:
                return True

    # Check diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player:
                return True
            if board[row][col + 3] == board[row + 1][col + 2] == board[row + 2][col + 1] == board[row + 3][col] == player:
                return True

    return False

def is_draw():
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    current_player = random.randint(0, PLAYERS - 1)
    while True:
        print_board()
        col = input("Player {}, please enter a column: ".format(CHECKERS[current_player]))
        if not col.isalpha() or col.upper() not in 'ABCDEFG':
            print("Invalid input. Please try again.")
            continue
        col = ord(col.upper()) - ord('A')
        if not is_valid_move(col):
            print("Column is full. Please try again.")
            continue
        make_move(CHECKERS[current_player], col)
        if check_win(CHECKERS[current_player]):
            print_board()
            print("Player {} won!".format(CHECKERS[current_player]))
            break
        elif is_draw():
            print_board()
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
