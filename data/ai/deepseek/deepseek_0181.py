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
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    border = '+' + '---+' * COLS
    print(border)
    for row in board:
        print('| ' + ' | '.join(cell for cell in row) + ' |')
        print(border)

def get_valid_column():
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not 'A' <= col <= chr(65 + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        return ord(col) - ord('A')

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
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
    col = get_valid_column()
    if not place_checker(board, col, CHECKERS[current_player]):
        print("Column is full. Try another column.")
        continue
    
    print_board(board)
    
    if check_win(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    
    if is_draw(board):
        print("It's a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
