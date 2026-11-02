import random
import os

ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def get_input(current_player):
    while True:
        col_input = input(f'Player {CHECKERS[current_player]}, please enter a column: ').upper()
        if len(col_input) == 1 and 'A' <= col_input <= 'G':
            return ord(col_input) - 65
        print("Invalid input, try again.")

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal \ 
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        print_board(board)
        col = get_input(current_player)
        if place_checker(board, col, CHECKERS[current_player]):
            if check_winner(board, CHECKERS[current_player]):
                print_board(board)
                print(f'Player {CHECKERS[current_player]} won!')
                break
            if check_draw(board):
                print_board(board)
                print('The game is a draw.')
                break
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Column is full, turn lost.")

main()
