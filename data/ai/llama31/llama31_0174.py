import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board():
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| ' + ' | '.join(row) + ' |')

def is_valid_input(column):
    if len(column)!= 1 or not 'A' <= column.upper() <= chr(64 + BOARD_COLS):
        return False
    column_index = ord(column.upper()) - 64
    for row in reversed(board):
        if row[column_index - 1] == ' ':
            return True
    return False

def place_checker(player, column):
    column_index = ord(column.upper()) - 64
    for row in reversed(board):
        if row[column_index - 1] == ' ':
            row[column_index - 1] = player
            break

def check_win(player):
    # Check horizontal locations for win
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

def check_draw():
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    players.remove(current_player)
    players.insert(0, current_player)

    while True:
        print_board()
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()
        while not is_valid_input(column):
            print("Invalid input. Please try again.")
            column = input().upper()
        place_checker(current_player, column)
        if check_win(current_player):
            print_board()
            print(f"Player {current_player} won!")
            break
        elif check_draw():
            print_board()
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
