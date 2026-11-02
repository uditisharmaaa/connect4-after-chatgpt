import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    for i in range(COLS):
        print(f'  {chr(65 + i)} ', end='')
    print()
    print('+---'*COLS + '+')
    for row in board:
        for cell in row:
            print(f'| {cell} ', end='')
        print('|')
        print('+---'*COLS + '+')

def select_first_player():
    return random.randint(0, PLAYERS - 1)

def is_valid_column(choice, cols):
    if choice.isalpha() and len(choice) == 1:
        col_index = ord(choice.upper()) - ord('A')
        return 0 <= col_index < cols
    return False

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal (Down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal (Down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

board = create_board(ROWS, COLS)
current_player = select_first_player()
print_board(board)

while True:
    checker = CHECKERS[current_player]
    col_choice = input(f"Player {checker}, please enter a column: ")

    while not is_valid_column(col_choice, COLS) or get_next_open_row(board, ord(col_choice.upper()) - ord('A')) is None:
        print("Invalid input! Please try again.")
        col_choice = input(f"Player {checker}, please enter a column: ")

    col_index = ord(col_choice.upper()) - ord('A')
    row_index = get_next_open_row(board, col_index)
    
    place_checker(board, row_index, col_index, checker)
    print_board(board)

    if check_win(board, checker):
        print(f"Player {checker} won!")
        break

    if is_draw(board):
        print("The game is a draw!")
        break

    current_player = (current_player + 1) % PLAYERS
