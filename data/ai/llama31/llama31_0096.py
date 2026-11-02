import os
import random
import string

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
board = [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

# Function to print the board
def print_board():
    os.system('clear')
    print('  ' + '   '.join(string.ascii_uppercase[:BOARD_COLUMNS]))
    print('+---' * BOARD_COLUMNS + '+')
    for row in board:
        print('|   ' * BOARD_COLUMNS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLUMNS + '+')
    print()

# Function to check for a win
def check_win(player_checker):
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == player_checker:
                return True
    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == player_checker:
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player_checker:
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player_checker:
                return True
    return False

# Function to check for a draw
def check_draw():
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Choose the first player randomly
current_player = random.randint(0, NUM_PLAYERS - 1)

# Main game loop
while True:
    print_board()
    print("Player " + CHECKERS[current_player] + ", please enter a column (A-" + string.ascii_uppercase[BOARD_COLUMNS-1] + "): ")
    col = input().upper()
    # Validate the input
    if len(col)!= 1 or not col.isalpha() or ord(col) - ord('A') < 0 or ord(col) - ord('A') >= BOARD_COLUMNS:
        print("Invalid input! Please enter a letter between A and " + string.ascii_uppercase[BOARD_COLUMNS-1] + ".")
        continue
    col_index = ord(col) - ord('A')
    # Place the checker at the correct location
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][col_index] == ' ':
            board[i][col_index] = CHECKERS[current_player]
            break
    else:
        print("Column is full! Please choose another column.")
        continue
    # Check for a win
    if check_win(CHECKERS[current_player]):
        print_board()
        print("Player " + CHECKERS[current_player] + " won!")
        break
    # Check for a draw
    if check_draw():
        print_board()
        print("It's a draw!")
        break
    # Switch to the next player
    current_player = (current_player + 1) % NUM_PLAYERS
