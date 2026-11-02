import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---+' * COLS)

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter from A to", chr(65 + COLS - 1))
            continue
        
        col_idx = ord(col) - ord('A')
        if col_idx < 0 or col_idx >= COLS:
            print("Invalid column. Please choose a column from A to", chr(65 + COLS - 1))
            continue
        
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_idx

def place_checker(board, col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row

def check_win(board, row, col, symbol):
    # Check horizontal
    count = 1
    # Left
    c = col - 1
    while c >= 0 and board[row][c] == symbol:
        count += 1
        c -= 1
    # Right
    c = col + 1
    while c < COLS and board[row][c] == symbol:
        count += 1
        c += 1
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    r = row - 1
    while r >= 0 and board[r][col] == symbol:
        count += 1
        r -= 1
    r = row + 1
    while r < ROWS and board[r][col] == symbol:
        count += 1
        r += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == symbol:
        count += 1
        r -= 1
        c -= 1
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == symbol:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True
    
    # Check diagonal (bottom-left to top-right)
    count = 1
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == symbol:
        count += 1
        r += 1
        c -= 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == symbol:
        count += 1
        r -= 1
        c += 1
    if count >= 4:
        return True
    
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialize game
board = initialize_board()
current_player = random.randint(0, PLAYERS - 1)
player_symbols = PLAYER_SYMBOLS[:PLAYERS]

# Game loop
while True:
    print_board(board)
    
    col_idx = get_valid_column(board)
    row = place_checker(board, col_idx, player_symbols[current_player])
    
    if check_win(board, row, col_idx, player_symbols[current_player]):
        print_board(board)
        print(f"Player {player_symbols[current_player]} won!")
        break
    
    if is_draw(board):
        print_board(board)
        print("It's a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
