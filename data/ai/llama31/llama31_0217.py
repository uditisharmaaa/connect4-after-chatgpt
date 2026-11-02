import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def print_board(board):
    os.system('clear')
    print('  A', ' B', ' C', ' D', ' E', ' F', ' G')
    for row in board:
        print('+---+' * COLUMNS)
        print('|', end='')
        for cell in row:
            print(' {} |'.format(cell), end='')
        print()
    print('+---+' * COLUMNS)

def is_valid_input(input_str):
    if len(input_str)!= 1 or input_str not in 'ABCDEFG':
        return False
    column_index = ord(input_str) - ord('A')
    return column_index < COLUMNS

def is_column_full(board, column_index):
    return board[0][column_index]!= ' '

def get_next_open_row(board, column_index):
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            return row_index
    return -1

def drop_checker(board, column_index, checker):
    next_open_row = get_next_open_row(board, column_index)
    if next_open_row == -1:
        return False
    board[next_open_row][column_index] = checker
    return True

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical
    for column in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][column] == checker and board[i + 1][column] == checker and board[i + 2][column] == checker and board[i + 3][column] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for column in range(COLUMNS - 3):
            if board[row][column] == checker and board[row + 1][column + 1] == checker and board[row + 2][column + 2] == checker and board[row + 3][column + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for column in range(COLUMNS - 3):
            if board[row][column] == checker and board[row - 1][column + 1] == checker and board[row - 2][column + 2] == checker and board[row - 3][column + 3] == checker:
                return True

    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_player = players[current_player_index]
        input_str = input('Player {}, please enter a column: '.format(current_player))

        if not is_valid_input(input_str):
            print('Invalid input. Please enter a letter between A and G.')
            continue

        column_index = ord(input_str) - ord('A')

        if is_column_full(board, column_index):
            print('Column is full. Please choose another column.')
            continue

        if not drop_checker(board, column_index, current_player):
            print('Error dropping checker. Please try again.')
            continue

        print_board(board)

        if check_win(board, current_player):
            print('Player {} won!'.format(current_player))
            break

        if check_draw(board):
            print('It\'s a draw!')
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == '__main__':
    main()
