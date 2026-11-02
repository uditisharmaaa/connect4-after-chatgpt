import random
import os

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    print('+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLS + '+')

def is_valid_move(board, column):
    return column >= 0 and column < COLS and board[0][column] == ' '

def make_move(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            break

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def get_valid_column():
    while True:
        try:
            col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
            if len(col_input) == 1 and 'A' <= col_input <= chr(64 + COLS):
                return ord(col_input) - 65
            print("Invalid input. Try again.")
        except:
            print("Invalid input. Try again.")

board = create_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

while True:
    column = get_valid_column()
    if is_valid_move(board, column):
        make_move(board, column, CHECKERS[current_player])
        print_board(board)
        
        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
            
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS
    else:
        print("Column is full. Turn lost.")
