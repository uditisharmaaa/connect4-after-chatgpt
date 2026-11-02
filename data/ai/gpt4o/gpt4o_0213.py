import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLS)]

# Initialize board
def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LABELS))
    print(('+' + '---' * COLS + '+'))
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---' * COLS + '+')

# Check valid input
def valid_input(column, board):
    if column in COLUMN_LABELS:
        index = COLUMN_LABELS.index(column)
        return board[0][index] == ' '
    return False

# Place checker
def place_checker(board, column, checker):
    index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[index] == ' ':
            row[index] = checker
            break

# Check for win
def check_win(board, checker):
    # Horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True
    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal (down-right and down-left)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

# Check for draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Game loop
def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        if valid_input(column, board):
            place_checker(board, column, current_checker)
            print_board(board)

            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            elif check_draw(board):
                print("The game is a draw.")
                break

            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Invalid input, please try again.")

play_game()
