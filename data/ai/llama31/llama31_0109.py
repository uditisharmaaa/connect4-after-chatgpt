import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, current_player):
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')
    print(f'Player {current_player}, please enter a column: ')

def is_valid_input(input_str):
    return len(input_str) == 1 and input_str.upper() in string.ascii_uppercase[:BOARD_COLS]

def get_column(input_str):
    return string.ascii_uppercase.index(input_str.upper())

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == checker:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True

    return False

def is_draw(board):
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    num_players = 2
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    while True:
        current_player = players[current_player_index]
        print_board(board, current_player)

        input_str = input().strip()
        while not is_valid_input(input_str):
            input_str = input("Invalid input. Please enter a column letter: ").strip()

        column = get_column(input_str)
        drop_checker(board, column, current_player)

        if check_win(board, current_player):
            print_board(board, current_player)
            print(f'Player {current_player} won!')
            break

        if is_draw(board):
            print_board(board, current_player)
            print('It\'s a draw!')
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
