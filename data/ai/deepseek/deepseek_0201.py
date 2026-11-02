import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS))
    print(header)
    
    # Print each row with separators
    separator = '+' + ('---+' * COLS)
    for row in board:
        print(separator)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print(separator)

def get_valid_column():
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or col_input < 'A' or col_input >= chr(65 + COLS):
            print(f"Invalid column. Please enter a letter from A to {chr(64 + COLS)}")
            continue
        col = ord(col_input) - 65
        return col

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, row, col, checker):
    # Check horizontal
    count = 1
    left, right = col - 1, col + 1
    while left >= 0 and board[row][left] == checker:
        count += 1
        left -= 1
    while right < COLS and board[row][right] == checker:
        count += 1
        right += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    up, down = row - 1, row + 1
    while up >= 0 and board[up][col] == checker:
        count += 1
        up -= 1
    while down < ROWS and board[down][col] == checker:
        count += 1
        down += 1
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    x, y = col - 1, row - 1
    while x >= 0 and y >= 0 and board[y][x] == checker:
        count += 1
        x -= 1
        y -= 1
    x, y = col + 1, row + 1
    while x < COLS and y < ROWS and board[y][x] == checker:
        count += 1
        x += 1
        y += 1
    if count >= 4:
        return True

    # Check diagonal (bottom-left to top-right)
    count = 1
    x, y = col - 1, row + 1
    while x >= 0 and y < ROWS and board[y][x] == checker:
        count += 1
        x -= 1
        y += 1
    x, y = col + 1, row - 1
    while x < COLS and y >= 0 and board[y][x] == checker:
        count += 1
        x += 1
        y -= 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialize the game
board = create_board()
current_player = random.randint(0, PLAYERS - 1)
player_checkers = CHECKERS[:PLAYERS]

print_board(board)

# Main game loop
while True:
    col = get_valid_column()
    if not place_checker(board, col, player_checkers[current_player]):
        print("Column is full. Turn lost.")
        continue
    
    print_board(board)
    
    # Find the row where the last checker was placed
    for row in range(ROWS):
        if board[row][col] == player_checkers[current_player]:
            placed_row = row
            break
    
    if check_win(board, placed_row, col, player_checkers[current_player]):
        print(f"Player {player_checkers[current_player]} won!")
        break
    
    if is_draw(board):
        print("It's a draw!")
        break
    
    # Switch to next player
    current_player = (current_player + 1) % PLAYERS
