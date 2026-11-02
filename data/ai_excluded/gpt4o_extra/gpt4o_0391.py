import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2  # Set as per requirement (2 to 5)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:MAX_PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

# Initialize the board
def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print('  ' + '   '.join(COLUMN_LABELS))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(' ' + cell + ' ' for cell in row) + '|')
    print('+---' * COLUMNS + '+')

# Check for a win condition
def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check down-right diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check up-right diagonal
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Check if the board is full
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Get valid column input from player
def get_valid_column_input(board, current_player):
    while True:
        try:
            column_input = input(f"Player {PLAYER_CHECKERS[current_player]}, please enter a column: ").strip().upper()
            if column_input not in COLUMN_LABELS:
                raise ValueError("Invalid column. Choose from " + ', '.join(COLUMN_LABELS))
            column_index = COLUMN_LABELS.index(column_input)
            if board[0][column_index] != ' ':
                raise ValueError("Column is full. Choose another one.")
            return column_index
        except ValueError as e:
            print(e)

# Place checker in the board column
def place_checker(board, column, current_player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = PLAYER_CHECKERS[current_player]
            break

# Main game loop
def main():
    board = initialize_board()
    current_player = random.randint(0, MAX_PLAYERS - 1)
    print_board(board)

    while True:
        column = get_valid_column_input(board, current_player)
        place_checker(board, column, current_player)
        print_board(board)

        if check_win(board, PLAYER_CHECKERS[current_player]):
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % MAX_PLAYERS

if __name__ == '__main__':
    main()
