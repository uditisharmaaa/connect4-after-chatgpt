import os
import random

# Constant variables
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS_COUNT]

# Function to create the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLUMNS)]))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * COLUMNS)

# Function to check for win
def check_for_win(board, checker):
    # Check horizontal, vertical and diagonal for win
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == checker:
                return True
    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == checker:
                return True
    # Diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True
    # Diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True

    return False

# Function to check for draw
def check_for_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Function to place checker
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

# Validate user input
def validate_input(input_column, board):
    if len(input_column) != 1 or not input_column.isalpha():
        return False
    col = ord(input_column.upper()) - ord('A')
    if col < 0 or col >= COLUMNS or board[0][col] != ' ':
        return False
    return True

# Main function to play game
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS_COUNT - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip()

        if not validate_input(user_input, board):
            print("Invalid input. Try again.")
            continue

        col = ord(user_input.upper()) - ord('A')
        if not place_checker(board, col, CHECKERS[current_player]):
            print("Column full. Turn skipped.")
            current_player = (current_player + 1) % PLAYERS_COUNT
            continue

        print_board(board)

        if check_for_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS_COUNT

play_game()
