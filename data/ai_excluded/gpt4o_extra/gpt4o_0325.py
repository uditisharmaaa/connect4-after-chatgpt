import os
import random

# Constants (Modify these for different dimensions or number of players)
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * COLS)

def get_input(valid_input):
    while True:
        choice = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if choice in valid_input:
            return ord(choice) - 65
        else:
            print("Invalid input. Try again.")

def is_valid_location(board, col):
    return board[0][col] == ' '

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            break

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal (both directions) for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == checker and all(board[r][c+i] == checker for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and all(board[r+i][c] == checker for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == checker and all(board[r+i][c+i] == checker for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == checker and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Game initialization
board = create_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

# Game loop
while True:
    col = get_input([chr(65 + i) for i in range(COLS) if is_valid_location(board, i)])
    place_checker(board, col, CHECKERS[current_player])
    print_board(board)

    if check_win(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    elif check_draw(board):
        print("It's a draw!")
        break

    current_player = (current_player + 1) % PLAYERS
