import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---+' * COLS)

def get_valid_column(board):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or column < 'A' or column > chr(65 + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        col_index = ord(column) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_index

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row][col+1] == checker and
                board[row][col+2] == checker and
                board[row][col+3] == checker):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and
                board[row+1][col] == checker and
                board[row+2][col] == checker and
                board[row+3][col] == checker):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == checker and
                board[row+1][col-1] == checker and
                board[row+2][col-2] == checker and
                board[row+3][col-3] == checker):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialize game
board = initialize_board()
current_player = random.choice(CHECKERS)
print_board(board)

# Game loop
while True:
    col = get_valid_column(board)
    place_checker(board, col, current_player)
    print_board(board)

    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        break

    if is_draw(board):
        print("Game ended in a draw!")
        break

    # Switch player
    current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]
