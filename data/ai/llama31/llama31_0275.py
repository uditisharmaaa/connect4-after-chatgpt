import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WINNING_CONDITION = 4

# Create the board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Function to print the board
def print_board():
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

# Function to validate user input
def validate_input(col):
    if not col.isalpha() or len(col)!= 1 or col not in string.ascii_uppercase[:BOARD_COLS]:
        return False
    col = ord(col) - ord('A')
    for row in reversed(board):
        if row[col] == ' ':
            return True
    return False

# Function to place a checker
def place_checker(col, player):
    col = ord(col) - ord('A')
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = CHECKERS[player]
            return

# Function to check for a win
def check_win(player):
    checker = CHECKERS[player]
    # Check horizontal
    for row in board:
        for i in range(len(row) - WINNING_CONDITION + 1):
            if all(cell == checker for cell in row[i:i + WINNING_CONDITION]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - WINNING_CONDITION + 1):
            if all(board[row][col] == checker for row in range(i, i + WINNING_CONDITION)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - WINNING_CONDITION + 1):
        for col in range(len(board[0]) - WINNING_CONDITION + 1):
            if all(board[row + i][col + i] == checker for i in range(WINNING_CONDITION)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(WINNING_CONDITION - 1, len(board)):
        for col in range(len(board[0]) - WINNING_CONDITION + 1):
            if all(board[row - i][col + i] == checker for i in range(WINNING_CONDITION)):
                return True
    return False

# Function to check for a draw
def check_draw():
    return all(all(cell!= ' ' for cell in row) for row in board)

# Main game loop
current_player = random.randint(0, NUM_PLAYERS - 1)
print_board()
while True:
    print("Player", CHECKERS[current_player], "please enter a column:")
    col = input().upper()
    if not validate_input(col):
        print("Invalid input, please try again.")
        continue
    place_checker(col, current_player)
    print_board()
    if check_win(current_player):
        print("Player", CHECKERS[current_player], "won!")
        break
    if check_draw():
        print("It's a draw!")
        break
    current_player = (current_player + 1) % NUM_PLAYERS
