import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for i, row in enumerate(board):
        print(f'+---+---+---+---+---+---+---+')
        print('| {} |'.format(' | '.join(row)))
    print(f'+---+---+---+---+---+---+---+')
    print('Player {}, please enter a column:'.format(CHECKERS[turn % PLAYERS]))

def is_valid_input(column):
    return 'A' <= column <= 'G' and 0 <= ord(column) - 65 < BOARD_COLS

def is_valid_move(board, column):
    return board[0][ord(column) - 65] == ' '

def get_next_open_row(board, column):
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][ord(column) - 65] == ' ':
            return row

def drop_piece(board, row, column, piece):
    board[row][ord(column) - 65] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def is_draw(board):
    return all(cell!= ' ' for row in board for cell in row)

board = create_board()
turn = random.randint(0, PLAYERS - 1)

while True:
    print_board(board)
    column = input().upper()
    while not is_valid_input(column) or not is_valid_move(board, column):
        if not is_valid_input(column):
            print('Invalid input. Please enter a letter between A and G.')
        else:
            print('Column is full. Please choose another column.')
        column = input().upper()

    row = get_next_open_row(board, column)
    drop_piece(board, row, column, CHECKERS[turn % PLAYERS])
    if winning_move(board, CHECKERS[turn % PLAYERS]):
        print_board(board)
        print('Player {} won!'.format(CHECKERS[turn % PLAYERS]))
        break
    elif is_draw(board):
        print_board(board)
        print('It\'s a draw!')
        break
    turn += 1
