import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the initial board with empty spaces
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(c) for c in range(65, 65 + COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

# Check if input is valid
def is_valid_input(input):
    return len(input) == 1 and input.isalpha() and 'A' <= input <= chr(65 + COLUMNS - 1)

# Place the checker in the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal for wins
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[r][col] == checker for r in range(row, row + 4)):
                return True

    # Diagonal right-down check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + r][col + r] == checker for r in range(4)):
                return True

    # Diagonal left-down check
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + r][col - r] == checker for r in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game function
def connect_four():
    board = create_board()
    current_player_index = random.choice(range(PLAYER_COUNT))
    checkers_playing = CHECKERS[:PLAYER_COUNT]

    while True:
        print_board(board)
        current_checker = checkers_playing[current_player_index]
        player_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        if not is_valid_input(player_input):
            print("Invalid input, please enter a valid column letter.")
            continue

        column = ord(player_input) - 65

        if not place_checker(board, column, current_checker):
            print("Column is full, you lose your turn.")
        else:
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == '__main__':
    connect_four()
