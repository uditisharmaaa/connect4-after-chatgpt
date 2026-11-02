import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the screen before printing the board
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_valid_column():
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col_num = ord(col) - ord('A')
        if col_num < 0 or col_num >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        if board[0][col_num] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_num

def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return (row, col)
    return None

def check_win(board, row, col, player):
    # Check horizontal
    count = 1
    # Left
    c = col - 1
    while c >= 0 and board[row][c] == player:
        count += 1
        c -= 1
    # Right
    c = col + 1
    while c < COLS and board[row][c] == player:
        count += 1
        c += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    # Up
    r = row - 1
    while r >= 0 and board[r][col] == player:
        count += 1
        r -= 1
    # Down (not needed as new piece is always at bottom)
    r = row + 1
    while r < ROWS and board[r][col] == player:
        count += 1
        r += 1
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == player:
        count += 1
        r -= 1
        c -= 1
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == player:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == player:
        count += 1
        r -= 1
        c += 1
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == player:
        count += 1
        r += 1
        c -= 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

# Initialize the game
board = initialize_board()
current_player = random.choice(CHECKERS)
print_board(board)

# Game loop
while True:
    col = get_valid_column()
    row, _ = place_checker(board, col, current_player)
    print_board(board)
    
    if check_win(board, row, col, current_player):
        print(f"Player {current_player} won!")
        break
    
    if is_draw(board):
        print("Game is a draw!")
        break
    
    # Switch player
    current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
