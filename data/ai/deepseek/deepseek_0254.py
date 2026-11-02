import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')
    # Print column letters
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print the board with borders
    for row in board:
        print('+' + '---+' * BOARD_COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * BOARD_COLS)

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col_num = ord(col) - ord('A')
        if col_num < 0 or col_num >= BOARD_COLS:
            print(f"Column out of range. Please enter a letter between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        if board[0][col_num] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_num

def place_checker(board, col, player):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col
    return -1, -1  # Shouldn't happen if input is validated

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
    while c < BOARD_COLS and board[row][c] == player:
        count += 1
        c += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    # Down
    r = row + 1
    while r < BOARD_ROWS and board[r][col] == player:
        count += 1
        r += 1
    # Up is not needed as we place from bottom
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
    while r < BOARD_ROWS and c < BOARD_COLS and board[r][c] == player:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True

    # Check diagonal (bottom-left to top-right)
    count = 1
    r, c = row + 1, col - 1
    while r < BOARD_ROWS and c >= 0 and board[r][c] == player:
        count += 1
        r += 1
        c -= 1
    r, c = row - 1, col + 1
    while r >= 0 and c < BOARD_COLS and board[r][c] == player:
        count += 1
        r -= 1
        c += 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

# Initialize game
board = initialize_board()
current_player = random.choice(PLAYERS)
print_board(board)

# Game loop
while True:
    col = get_valid_column(board)
    row, _ = place_checker(board, col, current_player)
    print_board(board)
    
    if check_win(board, row, col, current_player):
        print(f"Player {current_player} won!")
        break
    if is_draw(board):
        print("It's a draw!")
        break
    
    # Switch player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
