import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---+---+---+---+---+---+---+')

def validate_input(player, col):
    if not col.isalpha():
        return False
    if col.upper() not in string.ascii_uppercase[:BOARD_COLS]:
        return False
    if board[0][string.ascii_uppercase.index(col.upper())]!= ' ':
        return False
    return True

def place_checker(board, player, col):
    col = string.ascii_uppercase.index(col.upper())
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def check_win(board, player):
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

def check_draw(board):
    return ' ' not in [cell for row in board for cell in row]

def main():
    global board
    board = create_board()
    players = PLAYERS_CHECKERS[:2]  # Set to 2 players
    current_player = random.choice(players)
    while True:
        print_board(board)
        col = input(f"Player {current_player}, please enter a column: ")
        if not validate_input(current_player, col):
            print("Invalid input. Please try again.")
            continue
        place_checker(board, current_player, col)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()
