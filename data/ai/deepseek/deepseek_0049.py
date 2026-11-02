import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column letters
    print("  " + "   ".join([chr(i + 65) for i in range(COLS)]))
    
    # Print board rows
    for row in board:
        print("+" + "---+" * COLS)
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
    print("+" + "---+" * COLS)

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col > chr(65 + COLS - 1):
            print(f"Invalid column. Choose a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        col_index = ord(col) - 65
        if board[0][col_index] != " ":
            print("Column is full. Choose another column.")
            continue
        
        return col_index

def place_checker(board, col_index, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # Check horizontal
    count = 1
    left = col - 1
    while left >= 0 and board[row][left] == checker:
        count += 1
        left -= 1
    right = col + 1
    while right < COLS and board[row][right] == checker:
        count += 1
        right += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    down = row + 1
    while down < ROWS and board[down][col] == checker:
        count += 1
        down += 1
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True

    # Check diagonal (bottom-left to top-right)
    count = 1
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    return all(cell != " " for cell in board[0])

# Initialize game
board = initialize_board()
players = CHECKERS[:PLAYERS]
current_player = random.choice(players)
print_board(board)

# Game loop
while True:
    col_index = get_valid_column(board)
    row = place_checker(board, col_index, current_player)
    print_board(board)

    if check_win(board, row, col_index, current_player):
        print(f"Player {current_player} won!")
        break

    if is_draw(board):
        print("Game ended in a draw!")
        break

    # Switch to next player
    current_player = players[(players.index(current_player) + 1) % PLAYERS]
