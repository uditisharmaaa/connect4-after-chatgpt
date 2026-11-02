import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create an empty board
def create_board():
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + ' '.join([chr(65 + i) for i in range(NUM_COLS)]))
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * NUM_COLS + '+')

# Randomly select the first player
def select_first_player():
    return random.randint(0, NUM_PLAYERS - 1)

# Get the next player
def get_next_player(current_player):
    return (current_player + 1) % NUM_PLAYERS

# Validate user input
def validate_input(column):
    if not column.isalpha() or len(column)!= 1 or column.upper() < 'A' or column.upper() > chr(64 + NUM_COLS):
        return False
    return True

# Get the column index from user input
def get_column_index(column):
    return ord(column.upper()) - 65

# Check if a column is full
def is_column_full(board, column_index):
    return board[0][column_index]!= ' '

# Place a checker in a column
def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return

# Check for a win
def check_win(board, checker):
    # Check horizontal locations for win
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Main game loop
def game_loop():
    board = create_board()
    current_player = select_first_player()
    while True:
        print_board(board)
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ")
        while not validate_input(column):
            column = input("Invalid input. Please enter a column (A-{}): ".format(chr(64 + NUM_COLS)))
        column_index = get_column_index(column)
        if is_column_full(board, column_index):
            print("Column is full. Please try again.")
            continue
        place_checker(board, column_index, CHECKERS[current_player])
        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    game_loop()
