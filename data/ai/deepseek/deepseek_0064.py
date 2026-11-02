import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(COLS)])
    print(header)
    separator = "+" + ("---+" * COLS)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def get_valid_column():
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or column < 'A' or column > chr(ord('A') + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
            continue
        col_index = ord(column) - ord('A')
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Choose another column.")
            continue
        return col_index

def drop_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return row, col
    return -1, -1  # Shouldn't reach here if column is validated

def check_win(board, row, col):
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    player = board[row][col]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Initialize game
board = initialize_board()
current_player = random.choice(PLAYERS)
print_board(board)

# Game loop
while True:
    col = get_valid_column()
    row, _ = drop_checker(board, col, current_player)
    print_board(board)
    
    if check_win(board, row, col):
        print(f"Player {current_player} won!")
        break
    if is_draw(board):
        print("Game is a draw!")
        break
    
    # Switch to next player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
