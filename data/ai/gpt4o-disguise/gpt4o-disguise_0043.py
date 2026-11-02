import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_NAMES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(COLUMN_NAMES[:COLUMNS]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def valid_input(input_str):
    if input_str in COLUMN_NAMES[:COLUMNS]:
        return True
    return False

def update_board(board, col, checker):
    for i in range(ROWS-1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = checker
            return True
    return False

def win_check(board, checker):
    def check_direction(r_delta, c_delta):
        for r in range(ROWS):
            for c in range(COLUMNS):
                if all(0 <= r+i*r_delta < ROWS and 0 <= c+i*c_delta < COLUMNS and board[r+i*r_delta][c+i*c_delta] == checker for i in range(4)):
                    return True
        return False
    
    return (check_direction(0, 1) or check_direction(1, 0) or check_direction(1, 1) or check_direction(1, -1))

def draw_check(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_four():
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        while True:
            player_input = input().strip().upper()
            if valid_input(player_input) and update_board(board, COLUMN_NAMES.index(player_input), CHECKERS[current_player]):
                break
            print("Invalid input, try again or column full!")

        print_board(board)

        if win_check(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if draw_check(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

connect_four()
