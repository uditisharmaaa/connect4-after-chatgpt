import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(' ' + cell + ' ' for cell in row) + '|')
    print('+---' * COLUMNS + '+')

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                if col <= COLUMNS - 4 and all(board[row][col+i] == checker for i in range(4)):
                    return True
                if row <= ROWS - 4 and all(board[row+i][col] == checker for i in range(4)):
                    return True
                if row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                    return True
                if row >= 3 and col <= COLUMNS - 4 and all(board[row-i][col+i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_valid_column_choice():
    while True:
        choice = input("Player " + current_checker + ", please enter a column: ").strip().upper()
        if len(choice) == 1 and 'A' <= choice <= chr(64 + COLUMNS):
            return ord(choice) - 65
        print("Invalid input, try again.")

def main():
    board = initialize_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)
    print_board(board)

    while True:
        current_checker = players[players.index(current_player)]
        column_choice = get_valid_column_choice()

        if not drop_checker(board, column_choice, current_checker):
            print("The column is full, you lose your turn.")
            current_player = players[(players.index(current_player) + 1) % PLAYERS]
            continue

        print_board(board)

        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % PLAYERS]

main()
