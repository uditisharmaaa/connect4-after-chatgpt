import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    column_labels = '  '.join([chr(65 + i) for i in range(COLUMNS)])
    print('  ' + column_labels)
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * COLUMNS)

def is_valid_input(input_):
    return input_ in [chr(65 + i) for i in range(COLUMNS)]

def apply_gravity(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                if has_winning_sequence(board, row, col, checker):
                    return True
    return False

def has_winning_sequence(board, row, col, checker):
    return check_horizontal(board, row, col, checker) or check_vertical(board, row, col, checker) or check_diagonal(board, row, col, checker)

def check_horizontal(board, row, col, checker):
    count = 0
    for c in range(col, min(col + 4, COLUMNS)):
        if board[row][c] == checker:
            count += 1
        else:
            break
    return count == 4

def check_vertical(board, row, col, checker):
    count = 0
    for r in range(row, min(row + 4, ROWS)):
        if board[r][col] == checker:
            count += 1
        else:
            break
    return count == 4

def check_diagonal(board, row, col, checker):
    count1 = count2 = 0
    for i in range(4):
        if row + i < ROWS and col + i < COLUMNS and board[row + i][col + i] == checker:
            count1 += 1
        if row + i < ROWS and col - i >= 0 and board[row + i][col - i] == checker:
            count2 += 1
    return count1 == 4 or count2 == 4

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        current_checker = CHECKERS[current_player_index]
        column_input = input(f"Player {current_checker}, please enter a column: ").strip()
        while not is_valid_input(column_input):
            column_input = input(f"Invalid column. Player {current_checker}, please enter a valid column: ").strip()
        column = ord(column_input) - 65
        if apply_gravity(board, column, current_checker):
            print_board(board)
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
            current_player_index = (current_player_index + 1) % PLAYERS
        else:
            print(f"Column {column_input} is full. Player {current_checker} loses the turn.")
            current_player_index = (current_player_index + 1) % PLAYERS

play_game()
