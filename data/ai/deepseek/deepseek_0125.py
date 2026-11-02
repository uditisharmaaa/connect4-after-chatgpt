import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def get_valid_move(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha() or ord(col) - 65 not in range(COLS):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        col_idx = ord(col) - 65
        if board[0][col_idx] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_idx

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def check_win(board, row, col, checker):
    # Check horizontal
    for c in range(col - 3, col + 1):
        if c >= 0 and c + 3 < COLS and all(board[row][c + i] == checker for i in range(4)):
            return True
    # Check vertical
    for r in range(row - 3, row + 1):
        if r >= 0 and r + 3 < ROWS and all(board[r + i][col] == checker for i in range(4)):
            return True
    # Check diagonal (positive slope)
    for r, c in zip(range(row - 3, row + 1), range(col - 3, col + 1)):
        if r >= 0 and c >= 0 and r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
            return True
    # Check diagonal (negative slope)
    for r, c in zip(range(row - 3, row + 1), range(col + 3, col - 1, -1)):
        if r >= 0 and c - 3 >= 0 and r + 3 < ROWS and c < COLS and all(board[r + i][c - i] == checker for i in range(4)):
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Initialize game
board = create_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

# Game loop
while True:
    col = get_valid_move(board)
    row, _ = place_checker(board, col, CHECKERS[current_player])
    print_board(board)
    if check_win(board, row, col, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    if is_draw(board):
        print("It's a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
