import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_LABELS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLUMNS]

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LABELS[:len(board[0])]))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(row))

def get_valid_column_input(board):
    while True:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if column in COLUMN_LABELS[:len(board[0])] and not is_column_full(board, COLUMN_LABELS.index(column)):
            return COLUMN_LABELS.index(column)
        print("Invalid input. Please enter a valid column.")

def is_column_full(board, col):
    return all(board[row][col] != ' ' for row in range(len(board)))

def place_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row

def check_for_winner(board, checker):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == checker:
                for dr, dc in directions:
                    if check_direction(board, row, col, dr, dc, checker):
                        return True
    return False

def check_direction(board, row, col, dr, dc, checker):
    for i in range(1, 4):
        r, c = row + dr * i, col + dc * i
        if r < 0 or c < 0 or r >= len(board) or c >= len(board[0]) or board[r][c] != checker:
            return False
    return True

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(len(board[0])))

# Initialize board and game variables
board = create_board(ROWS, COLUMNS)
current_player = random.randint(0, PLAYERS - 1)

while True:
    print_board(board)
    column = get_valid_column_input(board)
    row = place_checker(board, column, CHECKERS[current_player])

    if check_for_winner(board, CHECKERS[current_player]):
        print_board(board)
        print(f"Player {CHECKERS[current_player]} won!")
        break
    if is_draw(board):
        print_board(board)
        print("The game is a draw!")
        break

    current_player = (current_player + 1) % PLAYERS
