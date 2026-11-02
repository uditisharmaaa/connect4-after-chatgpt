import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ']*columns for _ in range(rows)]

def print_board(board):
    print('  A B C D E F G')
    for row in board:
        print('+---'*(COLUMNS-1) + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---'*(COLUMNS-1) + '+')

def get_player_checker(player_index):
    return CHECKERS[player_index % len(CHECKERS)]

def is_valid_move(board, column):
    return board[0][column] == ' '

def make_move(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True
    # Check vertical
    for col in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True
    return False

def is_draw(board):
    return all([cell!= ' ' for row in board for cell in row])

def game():
    board = create_board(ROWS, COLUMNS)
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = 0
    while True:
        os.system('clear')
        print_board(board)
        print('Player', get_player_checker(players[current_player]), 'turn')
        column = input('Enter column (A-{}): '.format(chr(ord('A') + COLUMNS - 1)))
        column = ord(column) - ord('A')
        if not is_valid_move(board, column):
            print('Invalid move, try again')
            continue
        make_move(board, column, get_player_checker(players[current_player]))
        if check_win(board, get_player_checker(players[current_player])):
            os.system('clear')
            print_board(board)
            print('Player', get_player_checker(players[current_player]), 'won!')
            break
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print('It\'s a draw!')
            break
        current_player = (current_player + 1) % PLAYERS

game()
