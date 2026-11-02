import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
PLAYERS = ['X', 'O']
EMPTY_CELL = ' '

def create_board():
    return [[EMPTY_CELL for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(NUM_COLUMNS)))
    print('+---' * NUM_COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * NUM_COLUMNS + '+')

def is_valid_input(column):
    return column.isalpha() and 'A' <= column <= chr(ord('A') + NUM_COLUMNS - 1)

def is_valid_move(board, column_index):
    return board[0][column_index] == EMPTY_CELL

def place_checker(board, column_index, player):
    for row in reversed(board):
        if row[column_index] == EMPTY_CELL:
            row[column_index] = player
            return

def check_for_win(board, player):
    # Horizontal check
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == player:
                return True
    # Vertical check
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == player:
                return True
    # Diagonal checks
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True
        for col in range(3, NUM_COLUMNS):
            if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == player:
                return True
    return False

def check_for_draw(board):
    return all(cell != EMPTY_CELL for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()
        if not is_valid_input(column):
            continue
        column_index = ord(column) - ord('A')
        if not is_valid_move(board, column_index):
            continue

        place_checker(board, column_index, current_player)
        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

play_game()
