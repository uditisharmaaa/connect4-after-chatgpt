import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(header)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_input(column_input):
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    if ord(column_input) < ord('A') or ord(column_input) >= ord('A') + COLUMNS:
        return False
    return True

def drop_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal check (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    # Diagonal check (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    checkers_in_use = CHECKERS[:PLAYERS]

    while True:
        print_board(board)
        print(f"Player {checkers_in_use[current_player]}, please enter a column:")
        column_input = input().strip().upper()

        if not is_valid_input(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(column_input) - ord('A')

        if not drop_checker(board, column, checkers_in_use[current_player]):
            print("Column is full. Turn lost.")
            current_player = (current_player + 1) % PLAYERS
            continue

        if check_winner(board, checkers_in_use[current_player]):
            print_board(board)
            print(f"Player {checkers_in_use[current_player]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
